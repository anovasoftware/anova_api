import os
import sys
from dotenv import load_dotenv

# Only load .env if running locally
if os.getenv("ENVIRONMENT", "local") == "local":
    env_file = 'c:\\projects3\\anova_api\\.env'
    load_dotenv(env_file)

# env_file = 'c:\\projects3\\anova_api\\.env'
# load_dotenv(env_file)

DATABASE_KEY = os.getenv('DATABASE_KEY')
if not DATABASE_KEY:
    raise Exception("DATABASE_KEY environment variable not set.2")

# os.environ.setdefault("DATABASE_KEY", "local")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anova_api.settings')  # 🔁 Replace with actual module (e.g., 'anova_api.settings')

# ✅ Setup Django
import django
django.setup()

from core.utilities.token_utilities import initialize_tokens_from_env


def run():
    # initialize_tokens_from_env()
    # return
    manage_path = 'C:/Projects3/anova_api/manage.py'
    python_path = f'"{sys.executable}" '
    print(f'running manage.py commands 1: {python_path}')
    commands = []

    commands += [f'{manage_path} makemigrations']

    apps = ['static', 'base', 'res', 'bridge']

    commands.append(f'{manage_path} migrate authtoken')
    for app in apps:
        commands.append(f'{manage_path} migrate {app}')
        commands.append(f'{manage_path} loaddata {app}.json')

    # Removed token fixture
    # commands.append('manage.py loaddata authtoken_token.json')

    for command in commands:
        print(command)
        cmd = python_path + command
        os.system(cmd)

    print("Running token initialization from environment...")
    initialize_tokens_from_env()


if __name__ == '__main__':
    run()
