from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ==================== ENUMS ====================
class DisponibilidadeEnum(str, Enum):
    MANHA = "manhã"
    TARDE = "tarde"
    NOITE = "noite"
    FINAIS_SEMANA = "finais de semana"
    INTEGRAL = "integral"

class StatusEnum(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    PENDENTE = "pendente"

# ==================== MODELS ====================
class VoluntarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    telefone: str = Field(..., min_length=10)
    cargo_pretendido: str = Field(..., min_length=3)
    disponibilidade: DisponibilidadeEnum

class VoluntarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    telefone: Optional[str] = Field(None, min_length=10)
    cargo_pretendido: Optional[str] = Field(None, min_length=3)
    disponibilidade: Optional[DisponibilidadeEnum] = None
    status: Optional[StatusEnum] = None

class Voluntario(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str
    cargo_pretendido: str
    disponibilidade: DisponibilidadeEnum
    status: StatusEnum
    data_inscricao: datetime

# ==================== FAKE DATABASE ====================
fake_db: List[Voluntario] = []
counter = 1

# ==================== FASTAPI APP ====================
app = FastAPI(
    title="API Gerenciamento de Voluntários",
    description="Sistema CRUD para cadastro de voluntários",
    version="1.0.0"
)

# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "message": "API de Gerenciamento de Voluntários",
        "docs": "/docs"
    }

@app.post("/voluntarios", response_model=Voluntario, status_code=201)
def criar_voluntario(voluntario: VoluntarioCreate):
    """Cadastrar novo voluntário"""
    global counter
    
    # Verificar email duplicado
    if any(v.email == voluntario.email for v in fake_db):
        raise HTTPException(
            status_code=409, 
            detail="Email já cadastrado"
        )
    
    # Criar novo voluntário
    novo_voluntario = Voluntario(
        id=counter,
        nome=voluntario.nome,
        email=voluntario.email,
        telefone=voluntario.telefone,
        cargo_pretendido=voluntario.cargo_pretendido,
        disponibilidade=voluntario.disponibilidade,
        status=StatusEnum.ATIVO,
        data_inscricao=datetime.now()
    )
    
    fake_db.append(novo_voluntario)
    counter += 1
    
    return novo_voluntario

@app.get("/voluntarios", response_model=List[Voluntario])
def listar_voluntarios(
    status: Optional[StatusEnum] = Query(None, description="Filtrar por status"),
    cargo: Optional[str] = Query(None, description="Filtrar por cargo"),
    disponibilidade: Optional[DisponibilidadeEnum] = Query(None, description="Filtrar por disponibilidade")
):
    """Listar voluntários com filtros opcionais"""
    resultado = fake_db
    
    # Aplicar filtros
    if status:
        resultado = [v for v in resultado if v.status == status]
    
    if cargo:
        resultado = [v for v in resultado if cargo.lower() in v.cargo_pretendido.lower()]
    
    if disponibilidade:
        resultado = [v for v in resultado if v.disponibilidade == disponibilidade]
    
    return resultado

@app.get("/voluntarios/{id}", response_model=Voluntario)
def buscar_voluntario(id: int):
    """Buscar voluntário específico por ID"""
    voluntario = next((v for v in fake_db if v.id == id), None)
    
    if not voluntario:
        raise HTTPException(
            status_code=404, 
            detail="Voluntário não encontrado"
        )
    
    return voluntario

@app.put("/voluntarios/{id}", response_model=Voluntario)
def atualizar_voluntario(id: int, dados: VoluntarioUpdate):
    """Atualizar dados do voluntário"""
    voluntario = next((v for v in fake_db if v.id == id), None)
    
    if not voluntario:
        raise HTTPException(
            status_code=404, 
            detail="Voluntário não encontrado"
        )
    
    # Atualizar apenas campos fornecidos
    dados_dict = dados.dict(exclude_unset=True)
    
    for campo, valor in dados_dict.items():
        setattr(voluntario, campo, valor)
    
    return voluntario

@app.delete("/voluntarios/{id}", status_code=204)
def deletar_voluntario(id: int):
    """Excluir voluntário (soft delete - marca como inativo)"""
    voluntario = next((v for v in fake_db if v.id == id), None)
    
    if not voluntario:
        raise HTTPException(
            status_code=404, 
            detail="Voluntário não encontrado"
        )
    
    # Soft delete: marcar como inativo
    voluntario.status = StatusEnum.INATIVO
    
    return None


