#
# pylint: disable=import-error
#

from google.cloud import secretmanager
import os

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv("PROJECT_ID")
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Fetch secrets
DB_USER = get_secret("db_user")
DB_PASSWORD = get_secret("db_password")
DB_NAME = os.getenv("DB_NAME", "my_database")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

# Database connection configuration
DB_SOCKET_PATH = f'/cloudsql/{INSTANCE_CONNECTION_NAME}'

SQLALCHEMY_DATABASE_URI = (
    f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}'
    f'?unix_sock={DB_SOCKET_PATH}/.s.PGSQL.5432'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
