# kargo/admin.py
from django.contrib import admin
from .models import Categoria, Fornecedor, Produto, MovimentacaoEstoque, Pedido, ItemPedido


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # list_display define as colunas da tabela no admin
    list_display = ['sku', 'nome', 'categoria', 'quantidade_atual', 'estoque_minimo']
    # list_filter adiciona filtros na barra lateral direita
    list_filter = ['categoria', 'fornecedor']
    search_fields = ['nome', 'sku']


# ItemPedido aparece como tabela inline dentro da tela de Pedido —
# assim você gerencia pedido + itens na mesma página, como deve ser.
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1  # quantas linhas em branco aparecem por padrão


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'fornecedor', 'status', 'data_pedido']
    list_filter = ['status', 'fornecedor']
    inlines = [ItemPedidoInline]


# Para os modelos mais simples, o registro básico já é suficiente por agora
admin.site.register(Categoria)
admin.site.register(Fornecedor)
admin.site.register(MovimentacaoEstoque)