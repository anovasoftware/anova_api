#!/usr/bin/env python3
import os
import sys
import time
import socket
import subprocess
from pathlib import Path

# -------------------------------------------------------------------
# Environment & Django setup
# -------------------------------------------------------------------
# Only load .env if explicitly running "locally" (not in docker)
ENVIRONMENT = os.getenv("ENVIRONMENT", "docker").lower()
if ENVIRONMENT == "local":
    # Optional: load local .env (path can be overridden with LOCAL_DOTENV)
    from dotenv import load_dotenv
    env_file = os.getenv("LOCAL_DOTENV", ".env")
    if Path(env_file).exists():
        load_dotenv(env_file)

DATABASE_KEY = os.getenv("DATABASE_KEY")
if not DATABASE_KEY:
    raise Exception("DATABASE_KEY environment variable not set.")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "anova_api.settings"))

import django  # noqa: E402
django.setup()

from core.utilities.token_utilities import initialize_tokens_from_env  # noqa: E402


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def wait_for_db(host: str, port: int, timeout: int = 120):
    """Wait until a TCP connection to the DB host:port succeeds."""
    start = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"PostgreSQL reachable at {host}:{port}")
                return
        except OSError:
            elapsed = int(time.time() - start)
            if elapsed >= timeout:
                raise TimeoutError(f"Timed out after {timeout}s waiting for DB at {host}:{port}")
            time.sleep(0.2)


def run_manage(*args, check=True):
    """Run manage.py with the current Python interpreter."""
    cmd = [sys.executable, "manage.py", *args]
    print(">", " ".join(cmd))
    return subprocess.run(cmd, check=check)


def file_exists(path_str: str) -> bool:
    return Path(path_str).is_file()


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def run():
    # DB wait (inside Docker, pass DB_HOST/DB_PORT via env or defaults)
    db_host = os.getenv("DB_HOST", "db")
    db_port = int(os.getenv("DB_PORT", "5432"))
    print(f"Waiting for PostgreSQL at {db_host}:{db_port} ...")
    wait_for_db(db_host, db_port)

    # Controls (all overridable via env)
    run_makemigrations = os.getenv("RUN_MAKEMIGRATIONS", "0") == "1"
    load_fixtures = os.getenv("LOAD_FIXTURES", "1") == "1"

    # Comma-separated list of apps to migrate/loaddata (defaults from your old script)
    apps_csv = os.getenv("DJANGO_APPS", "static,base,res,bridge")
    apps = [a.strip() for a in apps_csv.split(",") if a.strip()]

    # Migrations
    print("Applying database migrations...")
    if run_makemigrations:
        run_manage("makemigrations", "--noinput")

    # Migrate built-ins / specific apps
    run_manage("migrate", "--noinput")
    run_manage("migrate", "authtoken", "--noinput")

    for app in apps:
        run_manage("migrate", app, "--noinput")
        if load_fixtures:
            # Tries `<app>.json` in project root or `<app>/fixtures/<app>.json`
            fixture_candidates = [
                f"{app}.json",
                f"{app}/fixtures/{app}.json",
            ]
            loaded = False
            for fx in fixture_candidates:
                if file_exists(fx):
                    print(f"Loading fixture: {fx}")
                    try:
                        run_manage("loaddata", fx)
                        loaded = True
                        break
                    except subprocess.CalledProcessError as e:
                        print(f"loaddata {fx} failed with code {e.returncode}; continuing")
            if not loaded:
                print(f"No fixture found for app '{app}' (checked {fixture_candidates}); skipping.")

    # Custom initialization (tokens from env)
    print("Running token initialization from environment...")
    try:
        initialize_tokens_from_env()
    except Exception as exc:
        # Non-fatal; print and continue
        print(f"initialize_tokens_from_env failed: {exc}")

    print("Database bootstrap complete.")

    # Optionally start the server from this script (handy for an all-in-one entrypoint)
    if os.getenv("START_SERVER", "0") == "1":
        use_gunicorn = os.getenv("USE_GUNICORN", "0") == "1"
        host = os.getenv("DJANGO_RUNSERVER_HOST", "0.0.0.0")
        port = os.getenv("DJANGO_RUNSERVER_PORT", "8000")
        if use_gunicorn:
            workers = os.getenv("GUNICORN_WORKERS", "3")
            module = os.getenv("WSGI_MODULE", "anova_api.wsgi:application")
            cmd = ["gunicorn", module, "--bind", f"{host}:{port}", "--workers", workers]
        else:
            cmd = [sys.executable, "manage.py", "runserver", f"{host}:{port}"]
        print("Starting server:", " ".join(cmd))
        os.execvp(cmd[0], cmd)  # replace the process


if __name__ == "__main__":
    run()
