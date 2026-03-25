from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import UsuarioForm,LoginForm,EmpresaForm
from .services import criar_database_empresa
from .db_utils import registrar_db_empresa

def criar_empresa(request):
    form=EmpresaForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        empresa=form.save()
        criar_database_empresa(empresa)
        return redirect("login")
    return render(request,"accounts/empresa_form.html",{"form":form})


def registrar_empresa(request):
    form=EmpresaForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request,"registrar_empresa.html",{"form":form})


def registrar_usuario(request):
    form=UsuarioForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=form.save()
        login(request,user)
        return redirect("home")
    return render(request,"registrar_usuario.html",{"form":form})

def login_view(request):
    form=LoginForm(request,data=request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=form.get_user()
        login(request,user)

        # registra conexão da empresa automaticamente
        if hasattr(user,"empresa") and user.empresa:
            registrar_db_empresa(user.empresa)
        return redirect("home")
    return render(request,"login.html",{"form":form})


def logout_view(request):
    logout(request)
    return redirect("login")