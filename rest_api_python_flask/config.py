from os import environ

def get_env_db_url(DB_URL=None):
    if not DB_URL:
        DB_URL=environ.get('DB_URL')

    return DB_URL