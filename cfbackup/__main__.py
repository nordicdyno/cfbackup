#!/usr/bin/env python
"""The main entry point. Invoke as `cfbackup' or `python -m cfbackup'.
"""
import sys
from .core import main

if __name__ == '__main__':
    sys.exit(main())
