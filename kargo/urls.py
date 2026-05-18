# kargo/urls.py
from django.urls import path
from . import views

app_name = 'kargo'

urlpatterns = [

    # Dashboard — raiz do sistema
    path('', views.DashboardView.as_view(), name='dashboard'),

    # ── Produtos ──────────────────────────────────────────────────
    path('produtos/',                     views.ProdutoListView.as_view(),   name='produto_list'),
    path('produtos/novo/',                views.ProdutoCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/',            views.ProdutoDetailView.as_view(), name='produto_detail'),
    path('produtos/<int:pk>/editar/',     views.ProdutoUpdateView.as_view(), name='produto_update'),
    path('produtos/<int:pk>/excluir/',    views.ProdutoDeleteView.as_view(), name='produto_delete'),

    # ── Categorias ────────────────────────────────────────────────
    path('categorias/',                   views.CategoriaListView.as_view(),   name='categoria_list'),
    path('categorias/novo/',              views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/',   views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/excluir/',  views.CategoriaDeleteView.as_view(), name='categoria_delete'),

    # ── Fornecedores ──────────────────────────────────────────────
    path('fornecedores/',                  views.FornecedorListView.as_view(),   name='fornecedor_list'),
    path('fornecedores/novo/',             views.FornecedorCreateView.as_view(), name='fornecedor_create'),
    path('fornecedores/<int:pk>/',         views.FornecedorDetailView.as_view(), name='fornecedor_detail'),
    path('fornecedores/<int:pk>/editar/',  views.FornecedorUpdateView.as_view(), name='fornecedor_update'),
    path('fornecedores/<int:pk>/excluir/', views.FornecedorDeleteView.as_view(), name='fornecedor_delete'),

    # ── Movimentações ─────────────────────────────────────────────
    # Movimentações não têm edição nem exclusão intencionalmente —
    # são registros contábeis imutáveis. Erros se corrigem com ajustes.
    path('movimentacoes/',                views.MovimentacaoListView.as_view(),   name='movimentacao_list'),
    path('movimentacoes/nova/',           views.MovimentacaoCreateView.as_view(), name='movimentacao_create'),

    # ── Pedidos ───────────────────────────────────────────────────
    path('pedidos/',                      views.PedidoListView.as_view(),   name='pedido_list'),
    path('pedidos/novo/',                 views.PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/<int:pk>/',             views.PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedidos/<int:pk>/editar/',      views.PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedidos/<int:pk>/excluir/',     views.PedidoDeleteView.as_view(), name='pedido_delete'),
]