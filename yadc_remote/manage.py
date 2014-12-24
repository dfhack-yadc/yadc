#!/usr/bin/env python
import os
import sys

sys.path.append('.')
import yadc.util
yadc.util.update_path()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yadc_remote.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
