from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Avaliacao

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

@router.post("/", response_model=Avaliacao)
def create_avaliacao(avaliacao: Avaliacao, session: Session = Depends(get_session)):
    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)
    return avaliacao

@router.get("/", response_model=List[Avaliacao])
def list_avaliacoes(session: Session = Depends(get_session)):
    return session.exec(select(Avaliacao)).all()

# CRUD: Deletar (Delete)""
@router.delete("/{avaliacao_id}")
def delete_avaliacao(avaliacao_id: int, session: Session = Depends(get_session)):
    avaliacao_db = session.get(Avaliacao, avaliacao_id)
    if not avaliacao_db:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    
    session.delete(avaliacao_db)
    session.commit()
    return {"message": "Avaliação deletada com sucesso"}