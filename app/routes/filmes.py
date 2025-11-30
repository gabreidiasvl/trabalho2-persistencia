from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, col, func
from typing import List, Optional
from app.database import get_session
from app.models import Filme, Ator, Avaliacao

router = APIRouter(prefix="/filmes", tags=["Filmes"])


@router.post("/", response_model=Filme)
def create_filme(filme: Filme, session: Session = Depends(get_session)):
    session.add(filme)
    session.commit()
    session.refresh(filme)
    return filme

@router.get("/", response_model=List[Filme])
def read_filmes(
    skip: int = 0, 
    limit: int = 10, 
    ordenar_por: Optional[str] = Query("id", enum=["id", "titulo", "ano"], description="Campo para ordenar a lista"),
    session: Session = Depends(get_session)
):
    query = select(Filme)
    
    if ordenar_por == "titulo":
        query = query.order_by(Filme.titulo)
    elif ordenar_por == "ano":
        query = query.order_by(Filme.ano)
    else:
        query = query.order_by(Filme.id)
        
    return session.exec(query.offset(skip).limit(limit)).all()

@router.put("/{filme_id}", response_model=Filme)
def update_filme(filme_id: int, filme_dados: Filme, session: Session = Depends(get_session)):
    filme_db = session.get(Filme, filme_id)
    if not filme_db:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    filme_db.titulo = filme_dados.titulo
    filme_db.ano = filme_dados.ano
    filme_db.categoria = filme_dados.categoria
    
    session.add(filme_db)
    session.commit()
    session.refresh(filme_db)
    return filme_db

@router.delete("/{filme_id}")
def delete_filme(filme_id: int, session: Session = Depends(get_session)):
    filme_db = session.get(Filme, filme_id)
    if not filme_db:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    session.delete(filme_db)
    session.commit()
    return {"message": "Filme deletado com sucesso"}


@router.get("/buscar", response_model=List[Filme])
def buscar_filmes(q: str, session: Session = Depends(get_session)):
    return session.exec(select(Filme).where(col(Filme.titulo).icontains(q))).all()

@router.get("/ano/{ano}", response_model=List[Filme])
def filmes_por_ano(ano: int, session: Session = Depends(get_session)):
    return session.exec(select(Filme).where(Filme.ano == ano)).all()

@router.get("/{filme_id}", response_model=Filme)
def get_filme_por_id(filme_id: int, session: Session = Depends(get_session)):
    filme = session.get(Filme, filme_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@router.get("/estatisticas/total")
def contar_filmes(session: Session = Depends(get_session)):
    total = session.exec(select(func.count(Filme.id))).one()
    return {"total_filmes": total}[]
@router.get("/estatisticas/por-categoria")
def filmes_por_categoria(session: Session = Depends(get_session)):
    """Retorna a quantidade de filmes agrupados por categoria."""
    query = select(Filme.categoria, func.count(Filme.id)).group_by(Filme.categoria)
    resultado = session.exec(query).all()
    
    return [{"categoria": cat, "quantidade": qtd} for cat, qtd in resultado]

@router.get("/{filme_id}/atores", response_model=List[Ator])
def atores_do_filme(filme_id: int, session: Session = Depends(get_session)):
    filme = session.get(Filme, filme_id)
    if not filme: raise HTTPException(404, "Filme não encontrado")
    return filme.atores