"""Windows training process tree: nested Job Object, attached before any child runs.

Job accounting includes exited descendants. Closing the job kills its entire tree;
measurement errors raise rather than silently reporting zero usage.
"""
from __future__ import annotations

import ctypes
import os
import subprocess
from contextlib import contextmanager

import winjob


@contextmanager
def wave_lease(root, wave):
    """Exclusive wave lease; an abandoned lease is never silently cleared."""
    if not isinstance(wave, str) or not wave.isalnum():
        raise ValueError("wave must be a single alphanumeric name")
    directory = root / "waves"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{wave}.lock"
    lease = path.open("x", encoding="utf-8")
    try:
        lease.write(str(os.getpid()))
        lease.flush()
        yield
    finally:
        lease.close()
        path.unlink()


class TrainingProcess:
    """Popen-compatible training handle with accounting for launcher and descendants."""

    def __init__(self, args, **kwargs):
        self.job = winjob.k32.CreateJobObjectW(None, None)
        winjob._check(self.job, "CreateJobObjectW(training)")
        self.process = None
        try:
            limits = winjob.ExtendedLimit()
            limits.BasicLimitInformation.LimitFlags = winjob.LIMIT_KILL_ON_CLOSE
            winjob._check(winjob.k32.SetInformationJobObject(
                self.job, winjob.JOB_EXTENDED, ctypes.byref(limits), ctypes.sizeof(limits)),
                "SetInformationJobObject(training)")
            self.process = subprocess.Popen(
                args, creationflags=winjob.CREATE_SUSPENDED, **kwargs)
            winjob._check(winjob.k32.AssignProcessToJobObject(
                self.job, int(self.process._handle)), "AssignProcessToJobObject(training)")
            if winjob.ntdll.NtResumeProcess(int(self.process._handle)) != 0:
                raise winjob.MeterError("NtResumeProcess(training) failed")
        except BaseException:
            if self.process is not None:
                self.process.kill()
                self.process.wait()
            self.close()
            raise

    @property
    def returncode(self):
        return self.process.returncode

    def cpu_s(self) -> float:
        user, kernel, _ = winjob.job_cpu(self.job)
        return user + kernel

    def memory_bytes(self) -> int:
        """Peak per-process committed memory, including processes that already exited."""
        limits = winjob.ExtendedLimit()
        winjob._query(self.job, winjob.JOB_EXTENDED, limits)
        return int(limits.PeakProcessMemoryUsed)

    def poll(self):
        code = self.process.poll()
        return code if code is not None and winjob.job_cpu(self.job)[2] == 0 else None

    def terminate(self) -> None:
        if not winjob.terminate_and_drain(self.job):
            raise winjob.MeterError("training descendants did not terminate within 30 seconds")

    def wait(self):
        return self.process.wait()

    def close(self) -> None:
        if self.job:
            winjob._check(winjob.k32.CloseHandle(self.job), "CloseHandle(training job)")
            self.job = None
