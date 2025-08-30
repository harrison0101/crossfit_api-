from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="CrossFit Academy API")

# Modelo de atleta
class Atleta(BaseModel):
    id: int
    nome: str
    idade: int
    nivel: str  # iniciante, intermediario, avancado

# "Banco de dados" em memória
atletas_db: List[Atleta] = []

# Endpoint assíncrono para listar todos os atletas
@app.get("/atletas", response_model=List[Atleta])
async def listar_atletas():
    return atletas_db

# Endpoint assíncrono para adicionar um atleta
@app.post("/atletas", response_model=Atleta)
async def adicionar_atleta(atleta: Atleta):
    for a in atletas_db:
        if a.id == atleta.id:
            raise HTTPException(status_code=400, detail="Atleta com esse ID já existe")
    atletas_db.append(atleta)
    return atleta

# Endpoint assíncrono para buscar um atleta por ID
@app.get("/atletas/{atleta_id}", response_model=Atleta)
async def buscar_atleta(atleta_id: int):
    for atleta in atletas_db:
        if atleta.id == atleta_id:
            return atleta
    raise HTTPException(status_code=404, detail="Atleta não encontrado")

# Endpoint assíncrono para deletar um atleta por ID
@app.delete("/atletas/{atleta_id}")
async def remover_atleta(atleta_id: int):
    for atleta in atletas_db:
        if atleta.id == atleta_id:
            atletas_db.remove(atleta)
            return {"detail": "Atleta removido com sucesso"}
    raise HTTPException(status_code=404, detail="Atleta não encontrado")
