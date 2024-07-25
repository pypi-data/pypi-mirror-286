import os
import sys
import sqlite3
from datetime import datetime

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seele_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Run the server
    execute_from_command_line(sys.argv + ['runserver'])

if __name__ == '__main__':
    main()
