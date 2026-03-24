from django.db import models



class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    @classmethod
    def listar_categorias(cls):
        return cls.objects.all()

    @classmethod
    def buscar_categoria_por_id(cls, categoria_id):
        return cls.objects.get(id=categoria_id)

    @classmethod
    def criar_categoria(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def atualizar_categoria(cls, categoria_id, data):
        categoria = cls.buscar_categoria_por_id(categoria_id)
        for campo, valor in data.items(): setattr(categoria, campo, valor)
        categoria.save()
        return categoria

    @classmethod
    def deletar_categoria(cls, categoria_id):
        cls.buscar_categoria_por_id(categoria_id).delete()



class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    @classmethod
    def listar_produtos(cls):
        return cls.objects.select_related("categoria").all()

    @classmethod
    def buscar_produto_por_id(cls, produto_id):
        return cls.objects.select_related("categoria").get(id=produto_id)

    @classmethod
    def criar_produto(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def atualizar_produto(cls, produto_id, data):
        produto = cls.buscar_produto_por_id(produto_id)
        for campo, valor in data.items(): setattr(produto, campo, valor)
        produto.save()
        return produto

    @classmethod
    def deletar_produto(cls, produto_id):
        cls.buscar_produto_por_id(produto_id).delete()



class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"

    @classmethod
    def listar_estoque(cls):
        return cls.objects.select_related("produto").all()

    @classmethod
    def buscar_estoque_por_produto(cls, produto_id):
        return cls.objects.select_related("produto").get(produto_id=produto_id)

    @classmethod
    def criar_estoque(cls, produto):
        return cls.objects.create(produto=produto, quantidade=0)

    @classmethod
    def atualizar_quantidade(cls, produto_id, quantidade):
        estoque = cls.buscar_estoque_por_produto(produto_id)
        estoque.quantidade = quantidade
        estoque.save()
        return estoque



class Movimentacao(models.Model):
    ENTRADA="E"; SAIDA="S"
    TIPO_CHOICES=[(ENTRADA,"Entrada"),(SAIDA,"Saída")]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.get_tipo_display()} - {self.quantidade}"

    @classmethod
    def listar_movimentacoes(cls):
        return cls.objects.select_related("produto").order_by("-data")

    @classmethod
    def registrar_entrada(cls, data):
        mov = cls.objects.create(**data, tipo=cls.ENTRADA)
        estoque = Estoque.buscar_estoque_por_produto(data["produto"].id)
        estoque.quantidade += data["quantidade"]
        estoque.save()
        return mov

    @classmethod
    def registrar_saida(cls, data):
        estoque = Estoque.buscar_estoque_por_produto(data["produto"].id)
        if estoque.quantidade < data["quantidade"]: raise ValueError("Estoque insuficiente")
        mov = cls.objects.create(**data, tipo=cls.SAIDA)
        estoque.quantidade -= data["quantidade"]
        estoque.save()
        return mov