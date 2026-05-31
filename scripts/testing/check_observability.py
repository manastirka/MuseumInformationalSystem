#!/usr/bin/env python3

"""Print the current runtime observability bootstrap status."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app


def main():
    status = app.extensions.get('observability_status', {})
    for integration, details in status.items():
        enabled = 'enabled' if details.get('enabled') else 'disabled'
        reason = details.get('reason', 'unknown')
        print(f'{integration}={enabled}:{reason}')


if __name__ == '__main__':
    main()
