import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seele_app.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management import call_command
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Run migrations
    call_command('migrate')

    # Start the server
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
