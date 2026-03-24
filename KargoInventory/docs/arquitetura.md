# Arquitetura do Sistema - Kargo

## 1. Visão Geral
O Inventum é uma aplicação web desenvolvida com Django, utilizando SQLite como banco de dados.

## 2. Padrão Arquitetural
O sistema segue uma arquitetura modular inspirada em microserviços, organizada em camadas:
- Views (camada de apresentação)
- Services (regras de negócio)
- Models (persistência)
- Repositories (acesso a dados)

## 3. Estrutura de Pastas
Descrever:
- inventory/models → entidades
- inventory/services → lógica de negócio
- inventory/views → controle
- inventory/templates → interface

## 4. Fluxo de Dados
Usuário → View → Service → Model → Banco de Dados

## 5. Tecnologias Utilizadas
- Python
- Django
- SQLite
- HTML/CSS

## 6. Considerações de Performance
- Uso de consultas otimizadas
- Separação de responsabilidades
- Redução de acoplamento
