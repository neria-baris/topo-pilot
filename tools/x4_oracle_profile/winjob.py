"""Win32 Job Object / process-time helpers for meter.py (ctypes, declared signatures)."""

from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import time

MEMORY_CAP = 8 * 1024**3


class BasicAccounting(ctypes.Structure):
    _fields_ = [
        ("TotalUserTime", ctypes.c_int64),
        ("TotalKernelTime", ctypes.c_int64),
        ("ThisPeriodTotalUserTime", ctypes.c_int64),
        ("ThisPeriodTotalKernelTime", ctypes.c_int64),
        ("TotalPageFaultCount", wt.DWORD),
        ("TotalProcesses", wt.DWORD),
        ("ActiveProcesses", wt.DWORD),
        ("TotalTerminatedProcesses", wt.DWORD),
    ]


class BasicLimit(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", wt.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wt.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wt.DWORD),
        ("SchedulingClass", wt.DWORD),
    ]


class ExtendedLimit(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", BasicLimit),
        ("IoInfo", ctypes.c_uint64 * 6),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class PidList(ctypes.Structure):
    _fields_ = [("Assigned", wt.DWORD), ("InList", wt.DWORD), ("Ids", ctypes.c_size_t * 64)]


class MemoryCounters(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD)] + [
        (name, ctypes.c_size_t)
        for name in (
            "PeakWorkingSetSize",
            "WorkingSetSize",
            "QuotaPeakPagedPoolUsage",
            "QuotaPagedPoolUsage",
            "QuotaPeakNonPagedPoolUsage",
            "QuotaNonPagedPoolUsage",
            "PagefileUsage",
            "PeakPagefileUsage",
        )
    ]


k32 = ctypes.WinDLL("kernel32", use_last_error=True)
ntdll = ctypes.WinDLL("ntdll")
psapi = ctypes.WinDLL("psapi", use_last_error=True)
_FT = ctypes.POINTER(wt.FILETIME)
for fn, args, res in (
    (k32.GetCurrentProcess, [], wt.HANDLE),
    (k32.GetProcessTimes, [wt.HANDLE, _FT, _FT, _FT, _FT], wt.BOOL),
    (k32.CreateJobObjectW, [ctypes.c_void_p, wt.LPCWSTR], wt.HANDLE),
    (k32.SetInformationJobObject, [wt.HANDLE, ctypes.c_int, ctypes.c_void_p, wt.DWORD], wt.BOOL),
    (
        k32.QueryInformationJobObject,
        [wt.HANDLE, ctypes.c_int, ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD)],
        wt.BOOL,
    ),
    (k32.AssignProcessToJobObject, [wt.HANDLE, wt.HANDLE], wt.BOOL),
    (k32.TerminateJobObject, [wt.HANDLE, wt.UINT], wt.BOOL),
    (k32.TerminateProcess, [wt.HANDLE, wt.UINT], wt.BOOL),
    (k32.WaitForSingleObject, [wt.HANDLE, wt.DWORD], wt.DWORD),
    (k32.CloseHandle, [wt.HANDLE], wt.BOOL),
    (k32.OpenProcess, [wt.DWORD, wt.BOOL, wt.DWORD], wt.HANDLE),
    (psapi.GetProcessMemoryInfo, [wt.HANDLE, ctypes.POINTER(MemoryCounters), wt.DWORD], wt.BOOL),
    (ntdll.NtResumeProcess, [wt.HANDLE], ctypes.c_long),
):
    fn.argtypes, fn.restype = args, res
JOB_ACCOUNTING, JOB_PID_LIST, JOB_EXTENDED = 1, 3, 9
LIMIT_JOB_MEMORY, LIMIT_KILL_ON_CLOSE = 0x200, 0x2000
CREATE_SUSPENDED, QUERY_LIMITED = 0x4, 0x1000


class MeterError(RuntimeError):
    pass


def _check(ok, what: str) -> None:
    if not ok:
        raise MeterError(f"{what} failed: WinError {ctypes.get_last_error()}")


def process_cpu_s(handle) -> float:
    times = [wt.FILETIME() for _ in range(4)]
    _check(k32.GetProcessTimes(handle, *[ctypes.byref(t) for t in times]), "GetProcessTimes")
    return sum((t.dwHighDateTime << 32) + t.dwLowDateTime for t in times[2:]) / 1e7


def own_cpu_s() -> float:
    return process_cpu_s(k32.GetCurrentProcess())


def _query(job, info_class: int, info) -> None:
    _check(
        k32.QueryInformationJobObject(
            job, info_class, ctypes.byref(info), ctypes.sizeof(info), None
        ),
        "QueryInformationJobObject",
    )


def job_cpu(job) -> tuple[float, float, int]:
    acct = BasicAccounting()
    _query(job, JOB_ACCOUNTING, acct)
    return acct.TotalUserTime / 1e7, acct.TotalKernelTime / 1e7, int(acct.ActiveProcesses)


def job_peak_working_set(job, seen: dict) -> None:
    """Peak working set of every live job process (polled; exited processes keep the last)."""
    pids = PidList()
    if not k32.QueryInformationJobObject(
        job, JOB_PID_LIST, ctypes.byref(pids), ctypes.sizeof(pids), None
    ):
        return
    for pid in pids.Ids[: pids.InList]:
        handle = k32.OpenProcess(QUERY_LIMITED, False, int(pid))
        if not handle:
            continue
        try:
            counters = MemoryCounters()
            counters.cb = ctypes.sizeof(counters)
            if psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
                seen[int(pid)] = max(seen.get(int(pid), 0), int(counters.PeakWorkingSetSize))
        finally:
            k32.CloseHandle(handle)


def make_job():
    job = k32.CreateJobObjectW(None, None)
    _check(job, "CreateJobObjectW")
    limits = ExtendedLimit()
    limits.BasicLimitInformation.LimitFlags = LIMIT_JOB_MEMORY | LIMIT_KILL_ON_CLOSE
    limits.JobMemoryLimit = MEMORY_CAP
    if not k32.SetInformationJobObject(
        job, JOB_EXTENDED, ctypes.byref(limits), ctypes.sizeof(limits)
    ):
        k32.CloseHandle(job)
        raise MeterError(f"SetInformationJobObject failed: WinError {ctypes.get_last_error()}")
    return job


def terminate_and_drain(job, timeout_s: float = 30.0) -> bool:
    """Terminate every job process and wait (bounded) until none is active."""
    k32.TerminateJobObject(job, 75)
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if job_cpu(job)[2] == 0:
            return True
        time.sleep(0.05)
    return False
