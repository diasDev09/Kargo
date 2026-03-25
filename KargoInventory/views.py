from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Produto,Categoria,Estoque,Movimentacao
from .forms import ProdutoForm,CategoriaForm,MovimentacaoForm
from django.contrib.auth.decorators import login_required


@login_required
def home(request):

    emp=request.user.empresa

    if not emp:
        return redirect("registrar_empresa")

    context={
    "total_produtos":Produto.listar_produtos_empresa(emp).count(),
    "estoque_baixo":Estoque.listar_estoque_baixo(emp).count(),
    "ultimas_movimentacoes":Movimentacao.listar_movimentacoes_empresa(emp)[:5]
    }

    return render(request,"home.html",context)

@login_required
def dashboard(request):
    emp=request.user.empresa
    if not emp:
        return redirect("registrar_empresa")
    context={
    "total_produtos":Produto.listar_produtos_empresa(emp).count(),
    "estoque_baixo":Estoque.listar_estoque_baixo(emp).count(),
    "movimentacoes":Movimentacao.listar_movimentacoes_empresa(emp)[:5]
    }
    return render(request,"dashboard.html",context)


@login_required
def produto(request):

    emp=request.user.empresa
    if not emp:
        return redirect("registrar_empresa")

    form=ProdutoForm(request.POST or None)

    if "deletar" in request.GET:
        Produto.deletar_produto(request.GET.get("deletar"),emp)
        return redirect("produto")

    if request.method=="POST" and form.is_valid():

        nome_categoria=form.cleaned_data.get("categoria_nome")

        categoria,_=Categoria.objects.using(emp.db_name).get_or_create(nome=nome_categoria)

        data=form.cleaned_data
        data["categoria"]=categoria

        produto=Produto.criar_produto(data,emp)

        Estoque.criar_estoque(produto,emp)

        return redirect("produto")

    context={
    "form":form,
    "produtos":Produto.listar_produtos_empresa(emp),
    "categorias":Categoria.objects.using(emp.db_name).all()
    }

    return render(request,"produto.html",context)


@login_required
def estoque(request):
    emp=request.user.empresa
    if not emp:
        return redirect("registrar_empresa")
    context={"estoque":Estoque.listar_estoque_empresa(emp)}
    return render(request,"estoque.html",context)


@login_required
def movimentacao(request):

    emp=request.user.empresa
    if not emp:
        return redirect("registrar_empresa")

    form=MovimentacaoForm(request.POST or None,empresa=emp)

    if request.method=="POST" and form.is_valid():

        try:

            if "entrada" in request.POST:
                Movimentacao.registrar_entrada(form.cleaned_data,emp)
                messages.success(request,"Entrada registrada")

            elif "saida" in request.POST:
                Movimentacao.registrar_saida(form.cleaned_data,emp)
                messages.success(request,"Saída registrada")

            return redirect("movimentacao")

        except ValueError as e:

            messages.error(request,str(e))

    context={
    "form":form,
    "movimentacoes":Movimentacao.listar_movimentacoes_empresa(emp)
    }

    return render(request,"movimentacao.html",context)