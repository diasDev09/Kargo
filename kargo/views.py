# kargo/views.py
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, F

from .models import Categoria, Fornecedor, Produto, MovimentacaoEstoque, Pedido


# ══════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'kargo/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_produtos']     = Produto.objects.count()
        context['total_categorias']   = Categoria.objects.count()
        context['total_fornecedores'] = Fornecedor.objects.count()
        # Produtos cujo estoque está no limite ou abaixo do mínimo
        context['produtos_criticos']  = Produto.objects.filter(
            quantidade_atual__lte=F('estoque_minimo')
        )
        # Últimas movimentações para o feed de atividade do dashboard
        context['ultimas_movimentacoes'] = MovimentacaoEstoque.objects.select_related(
            'produto', 'usuario'
        )[:8]
        return context


# ══════════════════════════════════════════════════════════════════
# PRODUTO
# ══════════════════════════════════════════════════════════════════

class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'kargo/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 20

    def get_queryset(self):
        # select_related faz um JOIN antecipado com Categoria e Fornecedor,
        # evitando o problema N+1 (uma query extra por produto no template).
        qs = Produto.objects.select_related('categoria', 'fornecedor')

        # Busca por nome ou SKU via parâmetro GET: /produtos/?q=caneta
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(nome__icontains=q) | qs.filter(sku__icontains=q)

        # Filtro por categoria via parâmetro GET: /produtos/?categoria=3
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            qs = qs.filter(categoria_id=categoria_id)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Repassa os filtros ativos ao template para manter os campos preenchidos
        context['q']          = self.request.GET.get('q', '')
        context['categoria_id'] = self.request.GET.get('categoria', '')
        context['categorias'] = Categoria.objects.all()
        return context


class ProdutoDetailView(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'kargo/produto_detail.html'
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Histórico completo de movimentações desse produto específico
        context['movimentacoes'] = self.object.movimentacoes.select_related('usuario')[:20]
        return context


class ProdutoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Produto
    template_name = 'kargo/produto_form.html'
    fields = [
        'nome', 'sku', 'descricao',
        'preco_custo', 'preco_venda',
        'quantidade_atual', 'estoque_minimo', 'estoque_maximo',
        'categoria', 'fornecedor',
    ]
    success_message = "Produto '%(nome)s' criado com sucesso!"
    success_url = reverse_lazy('kargo:produto_list')


class ProdutoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Produto
    template_name = 'kargo/produto_form.html'
    fields = [
        'nome', 'sku', 'descricao',
        'preco_custo', 'preco_venda',
        # quantidade_atual é omitida aqui de propósito — o estoque só
        # deve mudar via MovimentacaoEstoque, nunca por edição direta.
        'estoque_minimo', 'estoque_maximo',
        'categoria', 'fornecedor',
    ]
    success_message = "Produto '%(nome)s' atualizado com sucesso!"

    def get_success_url(self):
        # Após editar, volta para o detalhe do próprio produto
        return reverse_lazy('kargo:produto_detail', kwargs={'pk': self.object.pk})


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'kargo/produto_confirm_delete.html'
    context_object_name = 'produto'
    success_url = reverse_lazy('kargo:produto_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Produto excluído com sucesso.")
        return super().post(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════════
# CATEGORIA
# ══════════════════════════════════════════════════════════════════

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'kargo/categoria_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        # annotate() adiciona um campo calculado na query SQL — muito mais
        # eficiente do que chamar categoria.produtos.count() no template.
        return Categoria.objects.annotate(num_produtos=Count('produtos'))


class CategoriaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Categoria
    template_name = 'kargo/categoria_form.html'
    fields = ['nome', 'descricao']
    success_message = "Categoria '%(nome)s' criada com sucesso!"
    success_url = reverse_lazy('kargo:categoria_list')


class CategoriaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    template_name = 'kargo/categoria_form.html'
    fields = ['nome', 'descricao']
    success_message = "Categoria '%(nome)s' atualizada com sucesso!"
    success_url = reverse_lazy('kargo:categoria_list')


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'kargo/categoria_confirm_delete.html'
    context_object_name = 'categoria'
    success_url = reverse_lazy('kargo:categoria_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Categoria excluída com sucesso.")
        return super().post(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════════
# FORNECEDOR
# ══════════════════════════════════════════════════════════════════

class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'kargo/fornecedor_list.html'
    context_object_name = 'fornecedores'

    def get_queryset(self):
        return Fornecedor.objects.annotate(num_produtos=Count('produtos'))


class FornecedorDetailView(LoginRequiredMixin, DetailView):
    model = Fornecedor
    template_name = 'kargo/fornecedor_detail.html'
    context_object_name = 'fornecedor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = self.object.produtos.select_related('categoria')
        context['pedidos']  = self.object.pedidos.all()[:10]
        return context


class FornecedorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Fornecedor
    template_name = 'kargo/fornecedor_form.html'
    fields = ['nome', 'cnpj', 'telefone', 'email']
    success_message = "Fornecedor '%(nome)s' criado com sucesso!"
    success_url = reverse_lazy('kargo:fornecedor_list')


class FornecedorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Fornecedor
    template_name = 'kargo/fornecedor_form.html'
    fields = ['nome', 'cnpj', 'telefone', 'email']
    success_message = "Fornecedor '%(nome)s' atualizado com sucesso!"

    def get_success_url(self):
        return reverse_lazy('kargo:fornecedor_detail', kwargs={'pk': self.object.pk})


class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'kargo/fornecedor_confirm_delete.html'
    context_object_name = 'fornecedor'
    success_url = reverse_lazy('kargo:fornecedor_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Fornecedor excluído com sucesso.")
        return super().post(request, *args, **kwargs)


# ══════════════════════════════════════════════════════════════════
# MOVIMENTAÇÃO DE ESTOQUE
# ══════════════════════════════════════════════════════════════════

class MovimentacaoListView(LoginRequiredMixin, ListView):
    model = MovimentacaoEstoque
    template_name = 'kargo/movimentacao_list.html'
    context_object_name = 'movimentacoes'
    paginate_by = 30

    def get_queryset(self):
        qs = MovimentacaoEstoque.objects.select_related('produto', 'usuario')

        # Filtro por tipo: /movimentacoes/?tipo=entrada
        tipo = self.request.GET.get('tipo', '').strip()
        if tipo:
            qs = qs.filter(tipo=tipo)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_ativo'] = self.request.GET.get('tipo', '')
        return context


class MovimentacaoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MovimentacaoEstoque
    template_name = 'kargo/movimentacao_form.html'
    fields = ['produto', 'tipo', 'quantidade', 'motivo']
    success_message = "Movimentação registrada com sucesso!"
    success_url = reverse_lazy('kargo:movimentacao_list')

    def form_valid(self, form):
        # Injeta o usuário logado antes de salvar — o template não precisa
        # exibir esse campo, ele é preenchido automaticamente aqui.
        form.instance.usuario = self.request.user
        return super().form_valid(form)


# ══════════════════════════════════════════════════════════════════
# PEDIDO
# ══════════════════════════════════════════════════════════════════

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'kargo/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 20

    def get_queryset(self):
        qs = Pedido.objects.select_related('fornecedor', 'criado_por')

        # Filtro por status: /pedidos/?status=rascunho
        status = self.request.GET.get('status', '').strip()
        if status:
            qs = qs.filter(status=status)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_ativo'] = self.request.GET.get('status', '')
        # Passa as choices do modelo para o template poder montar o filtro dinamicamente
        context['status_choices'] = Pedido.STATUS_CHOICES
        return context


class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'kargo/pedido_detail.html'
    context_object_name = 'pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # prefetch_related é usado aqui porque itens é uma relação reversa (M2M/FK reversa).
        # select_related funciona para FK direta; prefetch_related para relações reversas.
        context['itens'] = self.object.itens.select_related('produto').all()
        return context


class PedidoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pedido
    template_name = 'kargo/pedido_form.html'
    fields = ['fornecedor', 'status', 'data_entrega']
    success_message = "Pedido criado com sucesso!"

    def form_valid(self, form):
        # Registra quem criou o pedido automaticamente
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Após criar, vai direto para o detalhe onde poderá adicionar os itens
        return reverse_lazy('kargo:pedido_detail', kwargs={'pk': self.object.pk})


class PedidoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pedido
    template_name = 'kargo/pedido_form.html'
    fields = ['fornecedor', 'status', 'data_entrega']
    success_message = "Pedido atualizado com sucesso!"

    def get_success_url(self):
        return reverse_lazy('kargo:pedido_detail', kwargs={'pk': self.object.pk})


class PedidoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'kargo/pedido_confirm_delete.html'
    context_object_name = 'pedido'
    success_url = reverse_lazy('kargo:pedido_list')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Pedido excluído com sucesso.")
        return super().post(request, *args, **kwargs)