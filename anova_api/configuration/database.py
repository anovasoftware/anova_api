import os
from dotenv import load_dotenv

load_dotenv('.env')

DATABASE_ID = os.getenv('DATABASE_ID')
PASSWORD = os.getenv('ANOVA_DB_PASSWORD')
DATABASE_DEFINITIONS = {
    'local': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': f'anova-db-{DATABASE_ID}',
        'USER': 'postgres',
        'PASSWORD': PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432'
    },
}