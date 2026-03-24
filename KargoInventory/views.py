from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Produto,Categoria,Estoque,Movimentacao
from .forms import ProdutoForm,CategoriaForm,MovimentacaoForm

def home(request):
    context={"total_produtos":Produto.listar_produtos().count(),
             "estoque_baixo":Estoque.objects.filter(quantidade__lte=5).count(),
             "ultimas_movimentacoes":Movimentacao.listar_movimentacoes()[:5]}
    return render(request,"home.html",context)


def dashboard(request):
    context={"total_produtos":Produto.listar_produtos().count(),
             "estoque_baixo":Estoque.objects.filter(quantidade__lte=5).count(),
             "movimentacoes":Movimentacao.listar_movimentacoes()[:5]}
    return render(request,"dashboard.html",context)


def produto(request):
    form=ProdutoForm(request.POST or None)

    if "deletar" in request.GET:
        Produto.deletar_produto(request.GET.get("deletar"))
        return redirect("produto")

    if request.method=="POST" and form.is_valid():
        produto=Produto.criar_produto(form.cleaned_data)
        Estoque.criar_estoque(produto)
        return redirect("produto")

    context={"form":form,"produtos":Produto.listar_produtos()}
    return render(request,"produto.html",context)


def estoque(request):
    context={"estoque":Estoque.listar_estoque()}
    return render(request,"estoque.html",context)


def movimentacao(request):
    form=MovimentacaoForm(request.POST or None)

    if request.method=="POST" and form.is_valid():
        try:
            if "entrada" in request.POST:
                Movimentacao.registrar_entrada(form.cleaned_data)
                messages.success(request,"Entrada registrada")
            elif "saida" in request.POST:
                Movimentacao.registrar_saida(form.cleaned_data)
                messages.success(request,"Saída registrada")

            return redirect("movimentacao")

        except ValueError as e:
            messages.error(request,str(e))

    context={"form":form,"movimentacoes":Movimentacao.listar_movimentacoes()}
    return render(request,"movimentacao.html",context)