#!/usr/bin/env python3
"""Generate or check the deterministic code index in docs/code_index/ (see tools/code_index)."""
import sys

from code_index.build import main

if __name__ == "__main__":
    sys.exit(main())
