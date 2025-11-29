from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class FilmeAtor(SQLModel, table=True):
    filme_id: Optional[int] = Field(default=None, foreign_key="filme.id", primary_key=True)
    ator_id: Optional[int] = Field(default=None, foreign_key="ator.id", primary_key=True)

class Ator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    
    filmes: List["Filme"] = Relationship(back_populates="atores", link_model=FilmeAtor)

class Filme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(index=True)
    ano: int = Field(index=True)
    categoria: str
    
    atores: List[Ator] = Relationship(back_populates="filmes", link_model=FilmeAtor)
    
    avaliacoes: List["Avaliacao"] = Relationship(back_populates="filme")

class Avaliacao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nota: int = Field(ge=1, le=5)
    comentario: Optional[str] = None
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    
    filme_id: Optional[int] = Field(default=None, foreign_key="filme.id")
    filme: Optional[Filme] = Relationship(back_populates="avaliacoes")