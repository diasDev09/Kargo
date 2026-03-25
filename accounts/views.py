from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import UsuarioForm,LoginForm,EmpresaForm


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
        login(request,form.get_user())
        return redirect("home")
    return render(request,"login.html",{"form":form})


def logout_view(request):
    logout(request)
    return redirect("login")