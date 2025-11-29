from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, col, func
from typing import List
from app.database import get_session
from app.models import Filme, Ator

router = APIRouter(prefix="/filmes", tags=["Filmes"])

@router.post("/", response_model=Filme)
def create_filme(filme: Filme, session: Session = Depends(get_session)):
    session.add(filme)
    session.commit()
    session.refresh(filme)
    return filme

@router.get("/", response_model=List[Filme])
def read_filmes(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(Filme).offset(skip).limit(limit)).all()

@router.get("/buscar", response_model=List[Filme])
def buscar_filmes(q: str, session: Session = Depends(get_session)):
    return session.exec(select(Filme).where(col(Filme.titulo).icontains(q))).all()

@router.get("/ano/{ano}", response_model=List[Filme])
def filmes_por_ano(ano: int, session: Session = Depends(get_session)):
    return session.exec(select(Filme).where(Filme.ano == ano)).all()

@router.get("/contar")
def contar_filmes(session: Session = Depends(get_session)):
    total = session.exec(select(func.count(Filme.id))).one()
    return {"total": total}

@router.get("/{filme_id}/atores", response_model=List[Ator])
def atores_do_filme(filme_id: int, session: Session = Depends(get_session)):
    filme = session.get(Filme, filme_id)
    if not filme: raise HTTPException(404, "Filme não encontrado")
    return filme.atores

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