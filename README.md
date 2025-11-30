Trabalho Prático: API de Mídias (FastAPI + SQLModel)

Pré-requisitos

É necessário ter o Python 3.12+ e o gerenciador uv instalados.
Caso não tenha o uv, instale via terminal:
pip install uv

Instalar dependências:
uv sync

Criar as tabelas (migração):
uv run alembic upgrade head

Povoar o banco de dados:
uv run python populate_db.py

Iniciar o servidor:
uv run uvicorn app.main:app --reload