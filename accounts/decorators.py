from django.shortcuts import redirect
from functools import wraps

def empresa_required(view_func):

    @wraps(view_func)

    def wrapper(request,*args,**kwargs):

        if not getattr(request.user,"empresa",None):

            return redirect("registrar_empresa")

        return view_func(request,*args,**kwargs)

    return wrapper