#!/usr/bin/env python3
"""
init_database.py
Run once locally to bootstrap the DB when Postgres is in Docker.cls
- Applies migrations (optionally makemigrations)
- Loads fixtures for selected apps if present
- Initializes tokens from env
"""

import os
from pathlib import Path

# --- Environment / Django setup --------------------------------------------
ENVIRONMENT = os.getenv("ENVIRONMENT", "local").lower()

# If running locally, load .env next to manage.py unless already loaded
if ENVIRONMENT == "local":
    try:
        from dotenv import load_dotenv, find_dotenv
        env_path = find_dotenv(usecwd=True) or str(Path(__file__).resolve().parent / ".env")
        if env_path:
            load_dotenv(env_path)
    except Exception:
        pass

DATABASE_KEY = os.getenv("DATABASE_KEY")
if not DATABASE_KEY:
    raise Exception("DATABASE_KEY environment variable not set.")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anova_api.settings")

import django  # noqa: E402
django.setup()

# --- Imports that require Django to be set up -------------------------------
from django.core.management import call_command  # noqa: E402
from django.conf import settings  # noqa: E402
from core.utilities.token_utilities import initialize_tokens_from_env  # noqa: E402


def load_data_if_exists(fixture_path: Path) -> bool:
    """Attempt to loaddata if the fixture exists. Return True if loaded."""
    if fixture_path.is_file():
        print(f"Loading fixture: {fixture_path}")
        try:
            call_command("loaddata", str(fixture_path))
            return True
        except Exception as e:
            print(f"loaddata failed for {fixture_path}: {e}")
    return False


def run():
    # Controls
    run_makemigrations = os.getenv("RUN_MAKEMIGRATIONS", "0") == "1"
    apps = [a.strip() for a in os.getenv("DJANGO_APPS", "static,base,authtoken,res,bridge").split(",") if a.strip()]

    project_root = Path(settings.BASE_DIR) if hasattr(settings, "BASE_DIR") else Path(__file__).resolve().parent
    print(f"Project root: {project_root}")

    # --- Migrations ---------------------------------------------------------
    print("Applying database migrations...")
    # if run_makemigrations:
    call_command("makemigrations", "--noinput")
    # call_command("migrate", "--noinput")
    # call_command("migrate", "authtoken", "--noinput")

    for app in apps:
        # If specific per-app migrate is desired (not necessary, but mirrors your original)
        call_command("migrate", app, "--noinput")

        # Try common fixture locations:
        # candidates = [
        #     project_root / f"{app}.json",
        #     project_root / app / "fixtures" / f"{app}.json",
        # ]
        # p = f'{project_root}/apps/{app}/fixtures/{app}.json'
        p = project_root / "apps" / app / "fixtures" / f"{app}.json"
        loaded = load_data_if_exists(p)
        # loaded = any(loaddata_if_exists(p) for p in candidates)
        if not loaded:
            print(f'Fixture {p} not loaded.')

    # --- Token init ---------------------------------------------------------
    print("Running token initialization from environment...")
    try:
        initialize_tokens_from_env()
        print("Token initialization complete.")
    except Exception as exc:
        print(f"Token initialization failed: {exc}")

    print("Database initialization complete.")


if __name__ == "__main__":
    run()
