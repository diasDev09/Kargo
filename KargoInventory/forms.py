from django import forms
from .models import Categoria, Produto, Movimentacao



class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ["nome","descricao"]
        widgets = {
            "nome": forms.TextInput(attrs={"class":"form-control","placeholder":"Nome da categoria"}),
            "descricao": forms.Textarea(attrs={"class":"form-control","rows":3,"placeholder":"Descrição"})
        }

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        return nome.strip()



class ProdutoForm(forms.ModelForm):

    categoria_nome=forms.CharField(
    widget=forms.TextInput(attrs={"class":"form-control","list":"categorias"})
    )

    class Meta:
        model=Produto
        fields=["nome","descricao","preco","ativo"]

        widgets={
        "nome":forms.TextInput(attrs={"class":"form-control"}),
        "descricao":forms.Textarea(attrs={"class":"form-control","rows":3}),
        "preco":forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
        "ativo":forms.CheckboxInput(attrs={"class":"form-check-input"})
        }

    def clean_preco(self):
        preco=self.cleaned_data.get("preco")
        if preco<=0:
            raise forms.ValidationError("Preço deve ser maior que zero")
        return preco



class MovimentacaoForm(forms.ModelForm):

    def __init__(self,*args,empresa=None,**kwargs):
        super().__init__(*args,**kwargs)
        if empresa:
            self.fields["produto"].queryset=Produto.listar_produtos_empresa(empresa)


    class Meta:
        model=Movimentacao
        fields=["produto","quantidade"]
        widgets={
        "produto":forms.Select(attrs={"class":"form-select"}),
        "quantidade":forms.NumberInput(attrs={"class":"form-control","min":"1"})
        }


    def clean_quantidade(self):
        quantidade=self.cleaned_data.get("quantidade")
        if quantidade<=0: raise forms.ValidationError("Quantidade deve ser maior que zero")
        return quantidade