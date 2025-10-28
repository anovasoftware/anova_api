import os
from dotenv import load_dotenv

# Only load .env if running locally
if os.getenv("ENVIRONMENT", "local") == "local":
    load_dotenv('.env')

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
PASSWORD = os.getenv('DATABASE_PASSWORD')

# print(f"HOST: {HOST}")
# print(f"DATABASE ID: {DATABASE_ID}")

DATABASE_DEFINITIONS = {
    'local': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': "django.db.backends.postgresql",
        'NAME': DATABASE_NAME,
        'USER': 'postgres',
        'PASSWORD': PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '5432'
    },
    'production': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': 'postgres',
        'PASSWORD': PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '5432'
    },

    # 'local-docker': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': f'anova-db-{DATABASE_ID}',
    #     'USER': 'postgres',
    #     'PASSWORD': PASSWORD,
    #     'HOST': 'postgres',
    #     'PORT': '5432'
    # },
}


def get_database_property(property_key):
    database_key = os.getenv('DATABASE_KEY')
    value = None
    database_dict = DATABASE_DEFINITIONS[database_key]
    if property_key in database_dict:
        value = database_dict[property_key]

    return value
