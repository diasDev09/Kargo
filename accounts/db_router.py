class EmpresaRouter:

    def db_for_read(self,model,**hints):
        empresa=hints.get("empresa")
        if empresa:
            return empresa.db_name
        return "default"


    def db_for_write(self,model,**hints):
        empresa=hints.get("empresa")
        if empresa:
            return empresa.db_name
        return "default"


    def allow_migrate(self,db,app_label,model_name=None,**hints):
        if app_label=="accounts":
            return db=="default"
        return True