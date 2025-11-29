from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes import filmes, atores, avaliacoes

app = FastAPI(
    title="Trabalho Prático - Mídias",
    version="1.0"
)

app.include_router(filmes.router)
app.include_router(atores.router)
app.include_router(avaliacoes.router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")