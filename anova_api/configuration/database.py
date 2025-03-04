import os
from dotenv import load_dotenv

load_dotenv('.env')

HOST = os.getenv('HOST')
DATABASE_ID = os.getenv('DATABASE_ID')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE_DEFINITIONS = {
    'local': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': f'anova-db-{DATABASE_ID}',
        'USER': 'postgres',
        'PASSWORD': PASSWORD,
        'HOST': f'{HOST}',
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
