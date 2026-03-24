from django.contrib import admin
from .models import Produto, Categoria, Estoque, Movimentacao


# 🔹 Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao')
    search_fields = ('nome',)
    ordering = ('nome',)


# 🔹 Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'preco', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'ativo')
    ordering = ('nome',)
    list_per_page = 10

    # Otimização de performance
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('categoria')


# 🔹 Estoque
@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'quantidade')
    search_fields = ('produto__nome',)
    ordering = ('produto__nome',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('produto')


# 🔹 Movimentação
@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'tipo', 'quantidade', 'data')
    list_filter = ('tipo', 'data')
    search_fields = ('produto__nome',)
    ordering = ('-data',)
    list_per_page = 15
    date_hierarchy = 'data'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('produto')

    # 🔒 Evita edição de movimentações (boas práticas)
    def has_change_permission(self, request, obj=None):
        return False