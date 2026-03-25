from django.db import models
from accounts.models import Empresa


class Categoria(models.Model):
    nome=models.CharField(max_length=100)
    descricao=models.TextField(blank=True,null=True)
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.nome

    @classmethod
    def listar_categorias_empresa(cls,empresa):
        return cls.objects.using(empresa.db_name).all()

    @classmethod
    def buscar_categoria_por_id(cls,categoria_id,empresa):
        return cls.objects.using(empresa.db_name).get(id=categoria_id)

    @classmethod
    def criar_categoria(cls,data,empresa):
        return cls.objects.using(empresa.db_name).create(**data,empresa=empresa)

    @classmethod
    def atualizar_categoria(cls,categoria_id,data,empresa):
        categoria=cls.buscar_categoria_por_id(categoria_id,empresa)
        for campo,valor in data.items(): setattr(categoria,campo,valor)
        categoria.save(using=empresa.db_name)
        return categoria

    @classmethod
    def deletar_categoria(cls,categoria_id,empresa):
        cls.objects.using(empresa.db_name).filter(id=categoria_id).delete()


class Produto(models.Model):
    nome=models.CharField(max_length=150)
    descricao=models.TextField(blank=True,null=True)
    preco=models.DecimalField(max_digits=10,decimal_places=2)
    categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE,null=True,blank=True)
    ativo=models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    @classmethod
    def listar_produtos_empresa(cls,empresa):
        return cls.objects.using(empresa.db_name).select_related("categoria").all()

    @classmethod
    def buscar_produto_por_id(cls,produto_id,empresa):
        return cls.objects.using(empresa.db_name).select_related("categoria").get(id=produto_id)

    @classmethod
    def criar_produto(cls,data,empresa):
        return cls.objects.using(empresa.db_name).create(**data,empresa=empresa)

    @classmethod
    def atualizar_produto(cls,produto_id,data,empresa):
        produto=cls.buscar_produto_por_id(produto_id,empresa)
        for campo,valor in data.items(): setattr(produto,campo,valor)
        produto.save(using=empresa.db_name)
        return produto

    @classmethod
    def deletar_produto(cls,produto_id,empresa):
        cls.objects.using(empresa.db_name).filter(id=produto_id).delete()


class Estoque(models.Model):
    produto=models.OneToOneField(Produto,on_delete=models.CASCADE)
    quantidade=models.IntegerField(default=0)
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.produto.nome}-{self.quantidade}"

    @classmethod
    def listar_estoque_empresa(cls,empresa):
        return cls.objects.using(empresa.db_name).select_related("produto").all()

    @classmethod
    def listar_estoque_baixo(cls,empresa):
        return cls.objects.using(empresa.db_name).filter(quantidade__lte=5)

    @classmethod
    def buscar_estoque_por_produto(cls,produto_id,empresa):
        return cls.objects.using(empresa.db_name).select_related("produto").get(produto_id=produto_id)

    @classmethod
    def criar_estoque(cls,produto,empresa):
        return cls.objects.using(empresa.db_name).create(produto=produto,empresa=empresa,quantidade=0)

    @classmethod
    def atualizar_quantidade(cls,produto_id,quantidade,empresa):
        estoque=cls.buscar_estoque_por_produto(produto_id,empresa)
        estoque.quantidade=quantidade
        estoque.save(using=empresa.db_name)
        return estoque


class Movimentacao(models.Model):
    ENTRADA="E";SAIDA="S"
    TIPO_CHOICES=[(ENTRADA,"Entrada"),(SAIDA,"Saída")]

    produto=models.ForeignKey(Produto,on_delete=models.CASCADE)
    tipo=models.CharField(max_length=1,choices=TIPO_CHOICES)
    quantidade=models.IntegerField()
    data=models.DateTimeField(auto_now_add=True)
    empresa=models.ForeignKey(Empresa,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.produto.nome}-{self.get_tipo_display()}-{self.quantidade}"

    @classmethod
    def listar_movimentacoes_empresa(cls,empresa):
        return cls.objects.using(empresa.db_name).select_related("produto").order_by("-data")

    @classmethod
    def registrar_entrada(cls,data,empresa):
        produto=data["produto"]
        qtd=data["quantidade"]
        estoque=Estoque.buscar_estoque_por_produto(produto.id,empresa)
        estoque.quantidade+=qtd
        estoque.save(using=empresa.db_name)
        return cls.objects.using(empresa.db_name).create(produto=produto,tipo=cls.ENTRADA,quantidade=qtd,empresa=empresa)

    @classmethod
    def registrar_saida(cls,data,empresa):
        produto=data["produto"]
        qtd=data["quantidade"]
        estoque=Estoque.buscar_estoque_por_produto(produto.id,empresa)
        if estoque.quantidade<qtd: raise ValueError("Estoque insuficiente")
        estoque.quantidade-=qtd
        estoque.save(using=empresa.db_name)
        return cls.objects.using(empresa.db_name).create(produto=produto,tipo=cls.SAIDA,quantidade=qtd,empresa=empresa)