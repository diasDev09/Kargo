# 📦 Kargo — Acesso ao Painel Administrativo

## 1. 🔐 Painel Admin do Django

O sistema possui um painel administrativo nativo do Django para gerenciamento de:
* Produtos
* Categorias
* Estoque
* Movimentações

### 🚀 Como acessar

Inicie o servidor:
```bash
python manage.py runserver
```

Acesse no navegador: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 2. 👤 Credenciais de acesso

O acesso ao painel é feito por um superusuário criado localmente.

Caso ainda não tenha criado, execute o comando abaixo:
```bash
python manage.py createsuperuser
```

Preencha os dados solicitados no terminal:
* **Username**
* **Email**
* **Senha**

---

## 3. 🧪 Ambiente de desenvolvimento (exemplo)

Para testes locais, você pode utilizar as seguintes credenciais:
* **Usuário:** `caiom`
* **Senha:** `abalaba`

> ⚠️ **Aviso:** Essas credenciais são apenas para ambiente de desenvolvimento e testes.

---

## 4. 🛠️ Funcionalidades disponíveis no Admin

* Cadastro e edição de produtos
* Associação com categorias
* Controle automático de estoque
* Registro de entradas e saídas
* Histórico de movimentações
* Filtros e buscas avançadas

---

## 📌 Observações

* Movimentações **não podem ser editadas** (isso garante a integridade do histórico).
* O estoque é atualizado automaticamente a cada movimentação.
* Interface otimizada com filtros e ordenação.

### 📚 Requisitos
* Python 3.x
* Django instalado
* Ambiente virtual ativo

---

## ▶️ Execução completa

```bash
# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Rodar servidor
python manage.py runserver
```

### ✔ Resultado esperado
Ao acessar o admin, você poderá gerenciar todo o sistema Inventum via interface web.
```
