from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Usuario,Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model=Empresa
        fields=["nome","cnpj"]
        widgets={
        "nome":forms.TextInput(attrs={"class":"form-control"}),
        "cnpj":forms.TextInput(attrs={"class":"form-control"})
        }


class UsuarioForm(UserCreationForm):
    class Meta:
        model=Usuario
        fields=["username","email","password1","password2","empresa"]
        widgets={
        "username":forms.TextInput(attrs={"class":"form-control"}),
        "email":forms.EmailInput(attrs={"class":"form-control"}),
        "empresa":forms.Select(attrs={"class":"form-select"})
        }


class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))