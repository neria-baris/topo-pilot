# Claude project instructions

## Automatic continuation after usage limits

The project owner requests that you implement and enable a persistent mechanism
that attempts to resume your unfinished, authorized work every five hours
(18,000 seconds), so work can continue after usage credits renew.

- Set up the mechanism while you can still execute tools. Use a durable external
  scheduler or supervisor that can launch Claude even after the current session
  stops; an instruction in this file or an in-session timer alone is insufficient.
- Before starting long-running work and at meaningful milestones, persist a
  checkpoint with the current task, progress, exact next steps, workspace, and
  session identifier when available. Have each scheduled attempt read it and
  resume the correct session or restore that context in a new session.
- Attempt continuation every five hours. If credits are still unavailable, record
  that outcome and leave the next attempt scheduled. Respect service limits; do
  not bypass them, switch accounts, or purchase credits automatically.
- Prevent overlapping runs with a lock and check for an already active worker
  before launching another. Keep a local log of attempts and outcomes.
- Continue only work already authorized by the owner, preserving existing project
  instructions and permissions. Stop attempts when that work is complete or the
  owner asks to stop; wait for owner input if further work requires it.
- Verify the scheduler is installed and enabled, check the checkpoint and resume
  command, and report its actual status, schedule, and how to disable it. Do not
  claim automatic continuation is active until the mechanism has been installed
  and checked. If setup is blocked, record the blocker and the remaining step.

## The public research summary is for external readers only

The owner approved this rule on 2026-10-20. Two locations hold the public summary of the research and its results:
- `00_READ_ME_FIRST_Research_Summary_So_Far/`, the PDF;
- `docs/research_summary/`, its LaTeX sources and figures.

Both are written for **external** readers and agents who visit the GitHub repository.

- **Project agents must not open, read, search or summarise these paths.** This covers coordinators, workers, implementation, author, test-author and reviewer subagents, and Codex reviews. Reading them would break the project's result-blind and independent roles.
- **Your source of truth is elsewhere.** Use the agent-handoff mailbox (COORDINATOR_STATE.md CURSOR, jobs/*), the protocols and the code.
- **One exception: the coordinator.** It rebuilds, checks and commits the document when the owner asks, and never passes its contents to other project agents.
- **When delegating,** do not attach or quote these paths in any prompt to another project agent.

## Code index (docs/code_index/)

The owner asked on 2026-10-21 for every agent to use and maintain the code index.

- **Look here first.** Before searching the tree for a file, function, caller or dependency, consult `docs/code_index/`: `FILES.md` (every tracked file), `files/<path>.md` (one page per code file: imports, imported-by, classes and functions with signatures and line numbers), `DEPENDENCIES.md` (dependency graph and tree), `FUNCTIONS*.md` (function key), `index.json` (machine-readable). Then open the source at the cited lines; the source stays the authority.
- **Keep it current.** After adding, removing, renaming or changing the imports or signatures of any tracked code file, run `.venv/Scripts/python.exe tools/build_code_index.py` and commit the regenerated `docs/code_index/` in its own commit (`docs(index): ...`) next to the code commit. Never edit the generated files by hand; change the generator instead (`tools/build_code_index.py` is the entry point; the code lives in `tools/code_index/`).
- **Check before relying on it.** `.venv/Scripts/python.exe tools/build_code_index.py --check` exits 1 if the index is stale; if so, regenerate before use.
- The index excludes the public research-summary paths named above; do not add them.
