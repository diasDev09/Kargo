import copy
from pathlib import Path
from django.conf import settings
from django.core.management import call_command
from django.utils import timezone
    
def registrar_db_empresa(empresa):

    if empresa.db_name in settings.DATABASES:
        return

    db_config=copy.deepcopy(settings.DATABASES["default"])

    db_config["NAME"]=Path(settings.BASE_DIR)/f"{empresa.db_name}.sqlite3"

    settings.DATABASES[empresa.db_name]=db_config