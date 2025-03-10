import os
import sys


def run():
    python_path = f'"{sys.executable}" '
    print(f'running manage.py commands 1: {python_path}')
    commands = []
    commands += ['manage.py makemigrations']

    apps = ['static', 'base', 'res', 'bridge']

    for app in apps:
        commands.append(f'manage.py migrate {app}')
        commands.append(f'manage.py loaddata {app}.json')

    commands.append(f'manage.py loaddata authtoken_token.json')
    # commands.append('manage.py migrate')
    # for command in commands:
    #     print(command)

    for command in commands:
        print(command)
        cmd = python_path + command
        os.system(cmd)

