import random
from sqlmodel import Session, select
from app.database import engine
from app.models import Filme, Ator, Avaliacao
from faker import Faker

fake = Faker('pt_BR')

def populate():
    print("Iniciando o povoamento do banco de dados...")
    
    with Session(engine) as session:
        midias_reais = [
            {"titulo": "O Poderoso Chefão", "tipo": "Filme"}, {"titulo": "Pulp Fiction", "tipo": "Filme"},
            {"titulo": "O Senhor dos Anéis: O Retorno do Rei", "tipo": "Filme"}, {"titulo": "Batman: O Cavaleiro das Trevas", "tipo": "Filme"},
            {"titulo": "A Origem", "tipo": "Filme"}, {"titulo": "Parasita", "tipo": "Filme"},
            {"titulo": "Matrix", "tipo": "Filme"}, {"titulo": "Cidade de Deus", "tipo": "Filme"},
            {"titulo": "A Viagem de Chihiro", "tipo": "Filme"}, {"titulo": "Interestelar", "tipo": "Filme"},
            {"titulo": "Breaking Bad", "tipo": "Série"}, {"titulo": "Game of Thrones", "tipo": "Série"},
            {"titulo": "Stranger Things", "tipo": "Série"}, {"titulo": "The Office", "tipo": "Série"},
            {"titulo": "Black Mirror", "tipo": "Série"}, {"titulo": "Dark", "tipo": "Série"},
            {"titulo": "Attack on Titan", "tipo": "Anime"}, {"titulo": "Death Note", "tipo": "Anime"},
            {"titulo": "Fullmetal Alchemist: Brotherhood", "tipo": "Anime"}, {"titulo": "Demon Slayer", "tipo": "Anime"},
            {"titulo": "Naruto", "tipo": "Anime"}, {"titulo": "Jujutsu Kaisen", "tipo": "Anime"},
            {"titulo": "Avenida Brasil", "tipo": "Novela"}, {"titulo": "O Clone", "tipo": "Novela"},
            {"titulo": "Senhora do Destino", "tipo": "Novela"}, {"titulo": "Vale Tudo", "tipo": "Novela"}
        ]

        comentarios_por_nota = {
            5: ["Perfeito! Uma obra-prima.", "Incrível, assistiria de novo.", "Recomendo para todo mundo!", "Sensacional!", "Top 10 da minha vida."],
            4: ["Muito bom, gostei bastante.", "Quase perfeito, vale muito a pena.", "Ótima história e personagens.", "Surpreendeu positivamente."],
            3: ["Bom, mas nada de especial.", "Divertido para passar o tempo.", "É ok, mas não me marcou.", "Tem seus altos e baixos."],
            2: ["Não gostei muito.", "Achei a premissa fraca.", "Esperava bem mais, foi uma decepção.", "Não funcionou pra mim."],
            1: ["Péssimo, perdi meu tempo.", "Não recomendo de jeito nenhum.", "Terrível, um dos piores que já vi.", "Muito ruim."]
        }

        print("Criando Atores...")
        atores_objs = []
        for _ in range(30):
            ator = Ator(nome=fake.name())
            session.add(ator)
            atores_objs.append(ator)
        
        session.commit()
        for ator in atores_objs: session.refresh(ator)

        print(f"Criando {len(midias_reais)} Filmes/Séries...")
        filmes_objs = []
        
        for midia in midias_reais:
            filme = Filme(
                titulo=midia["titulo"],
                categoria=midia["tipo"], 
                ano=random.randint(1990, 2023) 
            )
            filme.atores = random.sample(atores_objs, k=random.randint(2, 5))
            
            session.add(filme)
            filmes_objs.append(filme)
        
        session.commit()
        for f in filmes_objs: session.refresh(f)

        print("Criando Avaliações...")
        num_avaliacoes = 100
        
        for _ in range(num_avaliacoes):
            filme_escolhido = random.choice(filmes_objs)
            
            nota = random.randint(1, 5)
            
            texto_base = random.choice(comentarios_por_nota[nota])
            
            avaliacao = Avaliacao(
                nota=nota,
                comentario=texto_base,
                filme=filme_escolhido
            )
            session.add(avaliacao)

        session.commit()
        total_atores = session.exec(select(Ator)).all()
        total_filmes = session.exec(select(Filme)).all()
        total_avaliacoes = session.exec(select(Avaliacao)).all()

        print("\n--- Povoamento Concluído! ---")
        print(f"Total de Atores inseridos: {len(total_atores)}")
        print(f"Total de Mídias inseridas: {len(total_filmes)}")
        print(f"Total de Avaliações inseridas: {len(total_avaliacoes)}")

if __name__ == "__main__":
    populate()