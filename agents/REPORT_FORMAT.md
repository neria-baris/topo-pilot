# Report format (builders and test writers)

At most 150 words. Use these fields only. No narrative, no pasted logs.

```
MODULE: <name>            ROLE: builder | test-writer
STATUS: done | blocked | partial
FILES: <paths changed, one line>
TESTS: <command> -> <passed>/<total>, <seconds>s
SPEC DEVIATIONS: none | <item: what and why, ≤2 lines each>
AMBIGUITIES RESOLVED: none | <SPEC §: chosen reading>
OPEN RISKS: none | <≤3 bullets>
```

The conductor stores none of this in the repository. Decisions that matter go into `state/DECISIONS.md` as one line each.
