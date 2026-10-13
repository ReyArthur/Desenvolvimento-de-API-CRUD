from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Optional

app = FastAPI(
    title="API de Livros",
    description="API CRUD para gerenciar livros utilizando FastAPI e MongoDB",
    version="1.0.0"
)

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS (MongoDB)
# ==========================================
# Se estiver usando MongoDB Atlas, substitua a URI abaixo pela sua string de conexão.
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["biblioteca_db"]
colecao_livros = db["livros"]

# ==========================================
# MODELOS (Pydantic)
# ==========================================
class LivroCreate(BaseModel):
    titulo: str
    autor: str
    ano: int
    preco: float

class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    preco: Optional[float] = None

class LivroResponse(BaseModel):
    id: str
    titulo: str
    autor: str
    ano: int
    preco: float

# Função auxiliar para converter o documento do MongoDB no formato de resposta
def livro_helper(livro) -> dict:
    return {
        "id": str(livro["_id"]),
        "titulo": livro["titulo"],
        "autor": livro["autor"],
        "ano": livro["ano"],
        "preco": livro["preco"]
    }

# ==========================================
# ENDPOINTS (CRUD)
# ==========================================

# 1. CRIAR (POST)
@app.post("/livros/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(livro: LivroCreate):
    livro_dict = livro.model_dump()
    resultado = colecao_livros.insert_one(livro_dict)
    livro_criado = colecao_livros.find_one({"_id": resultado.inserted_id})
    return livro_helper(livro_criado)

# 2. CONSULTAR TODOS (GET)
@app.get("/livros/", response_model=List[LivroResponse], status_code=status.HTTP_200_OK)
def listar_livros():
    livros = colecao_livros.find()
    return [livro_helper(livro) for livro in livros]

# 3. CONSULTAR POR ID (GET)
@app.get("/livros/{id}", response_model=LivroResponse, status_code=status.HTTP_200_OK)
def buscar_livro(id: str):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID inválido.")
    
    livro = colecao_livros.find_one({"_id": obj_id})
    if livro:
        return livro_helper(livro)
    raise HTTPException(status_code=404, detail="Livro não encontrado.")

# 4. ATUALIZAR (PUT)
@app.put("/livros/{id}", response_model=LivroResponse, status_code=status.HTTP_200_OK)
def atualizar_livro(id: str, livro_atualizado: LivroUpdate):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID inválido.")
    
    # Filtra apenas os campos que foram preenchidos (não nulos)
    campos_para_atualizar = {k: v for k, v in livro_atualizado.model_dump().items() if v is not None}
    
    if len(campos_para_atualizar) >= 1:
        resultado = colecao_livros.update_one(
            {"_id": obj_id}, {"$set": campos_para_atualizar}
        )
        if resultado.matched_count == 0:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")
    
    livro = colecao_livros.find_one({"_id": obj_id})
    if livro:
        return livro_helper(livro)
    raise HTTPException(status_code=404, detail="Livro não encontrado.")

# 5. EXCLUIR (DELETE)
@app.delete("/livros/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_livro(id: str):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Formato de ID inválido.")
    
    resultado = colecao_livros.delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return None