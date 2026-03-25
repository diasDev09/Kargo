from .db_utils import registrar_db_empresa

class EmpresaMiddleware:

    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):

        if request.user.is_authenticated:

            if hasattr(request.user,"empresa") and request.user.empresa:

                registrar_db_empresa(request.user.empresa)

        response=self.get_response(request)

        return response