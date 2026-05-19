# kargo/seed.py

from django.contrib.auth.models import User
from django.utils import timezone
from kargo.models import (
    Categoria,
    Fornecedor,
    Produto,
    MovimentacaoEstoque,
    Pedido,
    ItemPedido
)


def run():

    # =========================
    # USUÁRIO
    # =========================
    user, created = User.objects.get_or_create(
        username='admin'
    )

    if created:
        user.set_password('123456')
        user.save()

    print("Usuário criado!")

    # =========================
    # CATEGORIAS
    # =========================
    categorias = [
        Categoria.objects.get_or_create(
            nome="Eletrônicos",
            descricao="Produtos eletrônicos"
        )[0],

        Categoria.objects.get_or_create(
            nome="Informática",
            descricao="Equipamentos de informática"
        )[0],

        Categoria.objects.get_or_create(
            nome="Periféricos",
            descricao="Acessórios e periféricos"
        )[0],

        Categoria.objects.get_or_create(
            nome="Escritório",
            descricao="Materiais de escritório"
        )[0],
    ]

    print("Categorias criadas!")

    # =========================
    # FORNECEDORES
    # =========================
    fornecedores = [
        Fornecedor.objects.get_or_create(
            nome="Tech Distribuidora",
            cnpj="12.345.678/0001-90",
            telefone="81999990001",
            email="contato@tech.com"
        )[0],

        Fornecedor.objects.get_or_create(
            nome="Mega Info",
            cnpj="98.765.432/0001-10",
            telefone="81999990002",
            email="vendas@megainfo.com"
        )[0],

        Fornecedor.objects.get_or_create(
            nome="Office Center",
            cnpj="11.222.333/0001-44",
            telefone="81999990003",
            email="suporte@office.com"
        )[0],
    ]

    print("Fornecedores criados!")

    # =========================
    # PRODUTOS
    # =========================
    produtos = [
        Produto.objects.get_or_create(
            sku="NOTE-001",
            defaults={
                "nome": "Notebook Dell Inspiron",
                "descricao": "Notebook 16GB RAM SSD 512GB",
                "preco_custo": 3200.00,
                "preco_venda": 4200.00,
                "quantidade_atual": 10,
                "estoque_minimo": 2,
                "estoque_maximo": 20,
                "categoria": categorias[1],
                "fornecedor": fornecedores[0],
            }
        )[0],

        Produto.objects.get_or_create(
            sku="MOUSE-001",
            defaults={
                "nome": "Mouse Gamer RGB",
                "descricao": "Mouse óptico gamer",
                "preco_custo": 50.00,
                "preco_venda": 120.00,
                "quantidade_atual": 35,
                "estoque_minimo": 5,
                "estoque_maximo": 100,
                "categoria": categorias[2],
                "fornecedor": fornecedores[1],
            }
        )[0],

        Produto.objects.get_or_create(
            sku="TECLADO-001",
            defaults={
                "nome": "Teclado Mecânico",
                "descricao": "Switch Blue ABNT2",
                "preco_custo": 140.00,
                "preco_venda": 280.00,
                "quantidade_atual": 15,
                "estoque_minimo": 3,
                "estoque_maximo": 50,
                "categoria": categorias[2],
                "fornecedor": fornecedores[1],
            }
        )[0],

        Produto.objects.get_or_create(
            sku="CADEIRA-001",
            defaults={
                "nome": "Cadeira Escritório Premium",
                "descricao": "Cadeira ergonômica",
                "preco_custo": 450.00,
                "preco_venda": 890.00,
                "quantidade_atual": 5,
                "estoque_minimo": 1,
                "estoque_maximo": 20,
                "categoria": categorias[3],
                "fornecedor": fornecedores[2],
            }
        )[0],
    ]

    print("Produtos criados!")

    # =========================
    # MOVIMENTAÇÕES
    # =========================
    MovimentacaoEstoque.objects.get_or_create(
        produto=produtos[0],
        tipo="entrada",
        quantidade=5,
        motivo="Reposição de estoque",
        usuario=user
    )

    MovimentacaoEstoque.objects.get_or_create(
        produto=produtos[1],
        tipo="saida",
        quantidade=2,
        motivo="Venda realizada",
        usuario=user
    )

    MovimentacaoEstoque.objects.get_or_create(
        produto=produtos[2],
        tipo="ajuste",
        quantidade=20,
        motivo="Inventário atualizado",
        usuario=user
    )

    print("Movimentações criadas!")

    # =========================
    # PEDIDOS
    # =========================
    pedido = Pedido.objects.get_or_create(
        fornecedor=fornecedores[0],
        status="confirmado",
        criado_por=user,
        data_pedido=timezone.now()
    )[0]

    ItemPedido.objects.get_or_create(
        pedido=pedido,
        produto=produtos[0],
        quantidade=3,
        preco_unitario=3200.00
    )

    ItemPedido.objects.get_or_create(
        pedido=pedido,
        produto=produtos[1],
        quantidade=10,
        preco_unitario=50.00
    )

    print("Pedidos criados!")

    print("Banco populado com sucesso!")