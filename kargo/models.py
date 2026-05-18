# kargo/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorias"
        ordering = ["nome"]


class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_atual = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0)
    estoque_maximo = models.IntegerField(default=0)

    # related_name='produtos' permite fazer categoria.produtos.all() nas views/templates
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='produtos'
    )
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='produtos'
    )

    def __str__(self):
        return f"[{self.sku}] {self.nome}"

    def estoque_critico(self):
        """Retorna True se o estoque está no limite ou abaixo do mínimo."""
        return self.quantidade_atual <= self.estoque_minimo

    def margem_lucro(self):
        """Calcula a margem de lucro percentual sobre o preço de custo."""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0

    class Meta:
        ordering = ["nome"]


class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("saida", "Saída"),
        ("ajuste", "Ajuste de inventário"),
    ]

    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='movimentacoes'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    motivo = models.TextField(blank=True)
    data_movimentacao = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='movimentacoes'
    )

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.produto.nome} ({self.quantidade})"

    def save(self, *args, **kwargs):
        """
        Sobrescreve o save padrão para atualizar o estoque do produto
        automaticamente sempre que uma movimentação for registrada.
        Isso garante que o estoque nunca seja alterado sem deixar rastro.
        """
        if self.tipo == "entrada":
            self.produto.quantidade_atual += self.quantidade
        elif self.tipo == "saida":
            self.produto.quantidade_atual -= self.quantidade
        elif self.tipo == "ajuste":
            # Ajuste define o valor absoluto, não incremental
            self.produto.quantidade_atual = self.quantidade
        self.produto.save()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-data_movimentacao"]
        verbose_name = "Movimentação de estoque"
        verbose_name_plural = "Movimentações de estoque"


# -----------------------------------------------------------------------------
# Pedido e ItemPedido ficam juntos porque ItemPedido não existe sem Pedido.
# É uma relação de composição: o item pertence inteiramente ao pedido pai.
# -----------------------------------------------------------------------------

class Pedido(models.Model):
    STATUS_CHOICES = [
        ("rascunho", "Rascunho"),
        ("enviado", "Enviado ao fornecedor"),
        ("confirmado", "Confirmado"),
        ("recebido", "Recebido"),
        ("cancelado", "Cancelado"),
    ]

    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.PROTECT, related_name='pedidos'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="rascunho")
    data_pedido = models.DateTimeField(default=timezone.now)
    data_entrega = models.DateTimeField(null=True, blank=True)
    criado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pedidos'
    )

    def __str__(self):
        return f"Pedido #{self.id} — {self.fornecedor.nome} ({self.get_status_display()})"

    def valor_total(self):
        """Soma os subtotais de todos os itens do pedido."""
        return sum(item.subtotal() for item in self.itens.all())

    class Meta:
        ordering = ["-data_pedido"]


class ItemPedido(models.Model):
    # related_name='itens' permite fazer pedido.itens.all() — muito mais legível
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_pedido')
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade}"