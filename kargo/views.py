# kargo/views.py

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count,F
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Categoria,Fornecedor,Produto,MovimentacaoEstoque,Pedido




# DASHBOARD

class DashboardView(TemplateView):
    template_name='kargo/dashboard.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['total_produtos']=Produto.objects.count()
        context['total_categorias']=Categoria.objects.count()
        context['total_fornecedores']=Fornecedor.objects.count()
        context['produtos_criticos']=Produto.objects.filter(
            quantidade_atual__lte=F('estoque_minimo')
        )
        context['ultimas_movimentacoes']=MovimentacaoEstoque.objects.select_related(
            'produto','usuario'
        )[:8]
        return context


# PRODUTOS

class ProdutoListView(ListView):
    model=Produto
    template_name='kargo/produto_list.html'
    context_object_name='produtos'
    paginate_by=20

    def get_queryset(self):
        qs=Produto.objects.select_related('categoria','fornecedor')

        q=self.request.GET.get('q','').strip()
        if q:
            qs=qs.filter(nome__icontains=q)|qs.filter(sku__icontains=q)

        categoria_id=self.request.GET.get('categoria')
        if categoria_id:
            qs=qs.filter(categoria_id=categoria_id)

        return qs

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        context['categoria_id']=self.request.GET.get('categoria','')
        context['categorias']=Categoria.objects.all()
        return context


class ProdutoDetailView(DetailView):
    model=Produto
    template_name='kargo/produto_detail.html'
    context_object_name='produto'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['movimentacoes']=self.object.movimentacoes.select_related('usuario')[:20]
        return context


class ProdutoCreateView(SuccessMessageMixin,CreateView):
    model=Produto
    template_name='kargo/produto_form.html'
    fields=[
        'nome','sku','descricao',
        'preco_custo','preco_venda',
        'quantidade_atual','estoque_minimo','estoque_maximo',
        'categoria','fornecedor'
    ]
    success_message="Produto '%(nome)s' criado com sucesso!"
    success_url=reverse_lazy('kargo:produto_list')


class ProdutoUpdateView(SuccessMessageMixin,UpdateView):
    model=Produto
    template_name='kargo/produto_form.html'
    fields=[
        'nome','sku','descricao',
        'preco_custo','preco_venda',
        'estoque_minimo','estoque_maximo',
        'categoria','fornecedor'
    ]
    success_message="Produto '%(nome)s' atualizado com sucesso!"

    def get_success_url(self):
        return reverse_lazy('kargo:produto_detail',kwargs={'pk':self.object.pk})


class ProdutoDeleteView(DeleteView):
    model=Produto
    template_name='kargo/produto_confirm_delete.html'
    context_object_name='produto'
    success_url=reverse_lazy('kargo:produto_list')

    def post(self,request,*args,**kwargs):
        messages.success(request,'Produto excluído com sucesso.')
        return super().post(request,*args,**kwargs)


# CATEGORIAS

class CategoriaListView(ListView):
    model=Categoria
    template_name='kargo/categoria_list.html'
    context_object_name='categorias'

    def get_queryset(self):
        return Categoria.objects.annotate(num_produtos=Count('produtos'))


class CategoriaCreateView(SuccessMessageMixin,CreateView):
    model=Categoria
    template_name='kargo/categoria_form.html'
    fields=['nome','descricao']
    success_message="Categoria '%(nome)s' criada com sucesso!"
    success_url=reverse_lazy('kargo:categoria_list')


class CategoriaUpdateView(SuccessMessageMixin,UpdateView):
    model=Categoria
    template_name='kargo/categoria_form.html'
    fields=['nome','descricao']
    success_message="Categoria '%(nome)s' atualizada com sucesso!"
    success_url=reverse_lazy('kargo:categoria_list')


class CategoriaDeleteView(DeleteView):
    model=Categoria
    template_name='kargo/categoria_confirm_delete.html'
    context_object_name='categoria'
    success_url=reverse_lazy('kargo:categoria_list')

    def post(self,request,*args,**kwargs):
        messages.success(request,'Categoria excluída com sucesso.')
        return super().post(request,*args,**kwargs)


# FORNECEDORES

class FornecedorListView(ListView):
    model=Fornecedor
    template_name='kargo/fornecedor_list.html'
    context_object_name='fornecedores'

    def get_queryset(self):
        return Fornecedor.objects.annotate(num_produtos=Count('produtos'))


class FornecedorDetailView(DetailView):
    model=Fornecedor
    template_name='kargo/fornecedor_detail.html'
    context_object_name='fornecedor'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['produtos']=self.object.produtos.select_related('categoria')
        context['pedidos']=self.object.pedidos.all()[:10]
        return context


class FornecedorCreateView(SuccessMessageMixin,CreateView):
    model=Fornecedor
    template_name='kargo/fornecedor_form.html'
    fields=['nome','cnpj','telefone','email']
    success_message="Fornecedor '%(nome)s' criado com sucesso!"
    success_url=reverse_lazy('kargo:fornecedor_list')


class FornecedorUpdateView(SuccessMessageMixin,UpdateView):
    model=Fornecedor
    template_name='kargo/fornecedor_form.html'
    fields=['nome','cnpj','telefone','email']
    success_message="Fornecedor '%(nome)s' atualizado com sucesso!"

    def get_success_url(self):
        return reverse_lazy('kargo:fornecedor_detail',kwargs={'pk':self.object.pk})


class FornecedorDeleteView(DeleteView):
    model=Fornecedor
    template_name='kargo/fornecedor_confirm_delete.html'
    context_object_name='fornecedor'
    success_url=reverse_lazy('kargo:fornecedor_list')

    def post(self,request,*args,**kwargs):
        messages.success(request,'Fornecedor excluído com sucesso.')
        return super().post(request,*args,**kwargs)


# MOVIMENTAÇÕES

class MovimentacaoListView(ListView):
    model=MovimentacaoEstoque
    template_name='kargo/movimentacao_list.html'
    context_object_name='movimentacoes'
    paginate_by=30

    def get_queryset(self):
        qs=MovimentacaoEstoque.objects.select_related('produto','usuario')

        tipo=self.request.GET.get('tipo','').strip()
        if tipo:
            qs=qs.filter(tipo=tipo)

        return qs

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tipo_ativo']=self.request.GET.get('tipo','')
        return context


class MovimentacaoCreateView(SuccessMessageMixin,CreateView):
    model=MovimentacaoEstoque
    template_name='kargo/movimentacao_form.html'
    fields=['produto','tipo','quantidade','motivo']
    success_message='Movimentação registrada com sucesso!'
    success_url=reverse_lazy('kargo:movimentacao_list')

    def form_valid(self,form):
        form.instance.usuario=self.request.user
        return super().form_valid(form)


# PEDIDOS

class PedidoListView(ListView):
    model=Pedido
    template_name='kargo/pedido_list.html'
    context_object_name='pedidos'
    paginate_by=20

    def get_queryset(self):
        qs=Pedido.objects.select_related('fornecedor','criado_por')

        status=self.request.GET.get('status','').strip()
        if status:
            qs=qs.filter(status=status)

        return qs

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['status_ativo']=self.request.GET.get('status','')
        context['status_choices']=Pedido.STATUS_CHOICES
        return context


class PedidoDetailView(DetailView):
    model=Pedido
    template_name='kargo/pedido_detail.html'
    context_object_name='pedido'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['itens']=self.object.itens.select_related('produto').all()
        return context


class PedidoCreateView(SuccessMessageMixin,CreateView):
    model=Pedido
    template_name='kargo/pedido_form.html'
    fields=['fornecedor','status','data_entrega']
    success_message='Pedido criado com sucesso!'

    def form_valid(self,form):
        form.instance.criado_por=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('kargo:pedido_detail',kwargs={'pk':self.object.pk})


class PedidoUpdateView(SuccessMessageMixin,UpdateView):
    model=Pedido
    template_name='kargo/pedido_form.html'
    fields=['fornecedor','status','data_entrega']
    success_message='Pedido atualizado com sucesso!'

    def get_success_url(self):
        return reverse_lazy('kargo:pedido_detail',kwargs={'pk':self.object.pk})


class PedidoDeleteView(DeleteView):
    model=Pedido
    template_name='kargo/pedido_confirm_delete.html'
    context_object_name='pedido'
    success_url=reverse_lazy('kargo:pedido_list')

    def post(self,request,*args,**kwargs):
        messages.success(request,'Pedido excluído com sucesso.')
        return super().post(request,*args,**kwargs)
