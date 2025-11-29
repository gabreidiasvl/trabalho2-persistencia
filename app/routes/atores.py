from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Ator, Filme
from fastapi import HTTPException 

router = APIRouter(prefix="/atores", tags=["Atores"])

@router.post("/", response_model=Ator)
def create_ator(ator: Ator, session: Session = Depends(get_session)):
    session.add(ator)
    session.commit()
    session.refresh(ator)
    return ator

@router.get("/", response_model=List[Ator])
def list_atores(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(Ator).offset(skip).limit(limit)).all()

@router.get("/{ator_id}/filmes", response_model=List[Filme])
def filmes_do_ator(ator_id: int, session: Session = Depends(get_session)):
    ator = session.get(Ator, ator_id)
    return ator.filmes if ator else []

@router.put("/{ator_id}", response_model=Ator)
def update_ator(ator_id: int, ator_dados: Ator, session: Session = Depends(get_session)):
    ator_db = session.get(Ator, ator_id)
    if not ator_db:
        raise HTTPException(status_code=404, detail="Ator não encontrado")
    
    ator_db.nome = ator_dados.nome
    session.add(ator_db)
    session.commit()
    session.refresh(ator_db)
    return ator_db

@router.delete("/{ator_id}")
def delete_ator(ator_id: int, session: Session = Depends(get_session)):
    ator_db = session.get(Ator, ator_id)
    if not ator_db:
        raise HTTPException(status_code=404, detail="Ator não encontrado")
    
    session.delete(ator_db)
    session.commit()
    return {"message": "Ator deletado com sucesso"}
    