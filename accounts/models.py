from django.db import models
from django.contrib.auth.models import AbstractUser


class Empresa(models.Model):
    nome=models.CharField(max_length=150)
    cnpj=models.CharField(max_length=20,unique=True)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.username