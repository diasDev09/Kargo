from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

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
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True
    )
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"[{self.sku}] {self.nome}"

    def estoque_critico(self):
        return self.quantidade_atual <= self.estoque_minimo

    def margem_lucro(self):
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

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    motivo = models.TextField(blank=True)
    data_movimentacao = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.tipo} — {self.produto.nome} ({self.quantidade})"

    def save(self, *args, **kwargs):
        # Atualiza o estoque do produto automaticamente ao salvar
        if self.tipo == "entrada":
            self.produto.quantidade_atual += self.quantidade
        elif self.tipo == "saida":
            self.produto.quantidade_atual -= self.quantidade
        elif self.tipo == "ajuste":
            self.produto.quantidade_atual = self.quantidade
        self.produto.save()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-data_movimentacao"]
        verbose_name = "Movimentação de estoque"
        verbose_name_plural = "Movimentações de estoque"


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("rascunho", "Rascunho"),
        ("enviado", "Enviado ao fornecedor"),
        ("confirmado", "Confirmado"),
        ("recebido", "Recebido"),
        ("cancelado", "Cancelado"),
    ]

    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="rascunho")
    data_pedido = models.DateTimeField(default=timezone.now)
    data_entrega = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} — {self.fornecedor.nome} ({self.status})"

    def valor_total(self):
        return sum(item.subtotal() for item in self.itempedido_set.all())

    class Meta:
        ordering = ["-data_pedido"]


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade}"