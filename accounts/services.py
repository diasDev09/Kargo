from django.conf import settings
from pathlib import Path


def criar_database_empresa(empresa):

    db_path=Path(settings.BASE_DIR)/f"{empresa.db_name}.sqlite3"

    settings.DATABASES[empresa.db_name]={
    "ENGINE":"django.db.backends.sqlite3",
    "NAME":db_path
    }