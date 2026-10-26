# Dota 2 — API de Heróis e Builds

Projeto de API desenvolvido com FastAPI para consultar heróis, itens e habilidades de Dota 2 e criar builds personalizadas. A interface web permite pesquisar heróis, visualizar imagens e selecionar itens, habilidades e passivas para montar uma build.

## Funcionalidades

- Consulta de heróis e imagens por meio da OpenDota.
- Consulta de itens com nome, ícone e custo.
- Consulta de habilidades com ícones e identificação de passivas.
- Criação, consulta, edição e exclusão de builds personalizadas.
- Armazenamento das builds em banco SQLite com SQLAlchemy.
- Proteção das operações de escrita por meio do cabeçalho `X-API-Key`.
- Interface web em HTML, CSS e JavaScript.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- OpenDota API
- HTML, CSS e JavaScript

## Estrutura do projeto

```text
dota2-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── heroes.py
│   │   └── builds.py
│   └── services/
│       ├── __init__.py
│       └── opendota.py
├── frontend/
│   └── index.html
├── .env.example                 # Exemplo de configuração
├── .gitignore
├── requirements.txt
└── dota2.db                     # Banco SQLite local