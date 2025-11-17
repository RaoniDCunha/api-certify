from fastapi.testclient import TestClient
from main import app, fake_db

client = TestClient(app)

# Limpar DB antes de cada teste
def setup_function():
    """Limpar banco de dados fake antes de cada teste"""
    fake_db.clear()
    globals()['counter'] = 1

# Testes

def test_criar_voluntario_valido():
    """Deve criar voluntário com dados válidos"""
    response = client.post("/voluntarios", json={
        "nome": "João Silva",
        "email": "joao@example.com",
        "telefone": "(11) 98765-4321",
        "cargo_pretendido": "Instrutor",
        "disponibilidade": "manhã"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["email"] == "joao@example.com"
    assert data["status"] == "ativo"
    assert "data_inscricao" in data
    assert "id" in data

def test_nao_permitir_email_duplicado():
    """Não deve permitir cadastro com email duplicado"""
    voluntario_data = {
        "nome": "Maria Santos",
        "email": "maria@example.com",
        "telefone": "(11) 91234-5678",
        "cargo_pretendido": "Coordenador",
        "disponibilidade": "tarde"
    }
    
    # Primeira criação - deve funcionar
    response1 = client.post("/voluntarios", json=voluntario_data)
    assert response1.status_code == 201
    
    # Segunda criação com mesmo email - deve falhar
    response2 = client.post("/voluntarios", json=voluntario_data)
    assert response2.status_code == 409
    assert "já cadastrado" in response2.json()["detail"].lower()

# ==================== TESTES ADICIONAIS ====================

def test_listar_voluntarios():
    """Deve listar todos os voluntários"""
    # Criar dois voluntários
    client.post("/voluntarios", json={
        "nome": "Pedro Costa",
        "email": "pedro@example.com",
        "telefone": "(11) 91111-1111",
        "cargo_pretendido": "Monitor",
        "disponibilidade": "noite"
    })
    
    client.post("/voluntarios", json={
        "nome": "Ana Lima",
        "email": "ana@example.com",
        "telefone": "(11) 92222-2222",
        "cargo_pretendido": "Apoio",
        "disponibilidade": "integral"
    })
    
    response = client.get("/voluntarios")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_buscar_voluntario_por_id():
    """Deve buscar voluntário específico por ID"""
    # Criar voluntário
    create_response = client.post("/voluntarios", json={
        "nome": "Carlos Souza",
        "email": "carlos@example.com",
        "telefone": "(11) 93333-3333",
        "cargo_pretendido": "Instrutor",
        "disponibilidade": "manhã"
    })
    
    voluntario_id = create_response.json()["id"]
    
    # Buscar por ID
    response = client.get(f"/voluntarios/{voluntario_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Carlos Souza"
    assert data["id"] == voluntario_id

def test_buscar_voluntario_inexistente():
    """Deve retornar 404 para voluntário inexistente"""
    response = client.get("/voluntarios/999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"].lower()

def test_atualizar_voluntario():
    """Deve atualizar dados do voluntário"""
    # Criar voluntário
    create_response = client.post("/voluntarios", json={
        "nome": "Fernanda Alves",
        "email": "fernanda@example.com",
        "telefone": "(11) 94444-4444",
        "cargo_pretendido": "Monitor",
        "disponibilidade": "tarde"
    })
    
    voluntario_id = create_response.json()["id"]
    
    # Atualizar
    update_response = client.put(f"/voluntarios/{voluntario_id}", json={
        "nome": "Fernanda Alves Santos",
        "cargo_pretendido": "Coordenador"
    })
    
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["nome"] == "Fernanda Alves Santos"
    assert data["cargo_pretendido"] == "Coordenador"
    assert data["email"] == "fernanda@example.com"  # Não mudou

def test_soft_delete():
    """Deve marcar voluntário como inativo ao deletar (soft delete)"""
    # Criar voluntário
    create_response = client.post("/voluntarios", json={
        "nome": "Roberto Lima",
        "email": "roberto@example.com",
        "telefone": "(11) 95555-5555",
        "cargo_pretendido": "Apoio",
        "disponibilidade": "finais de semana"
    })
    
    voluntario_id = create_response.json()["id"]
    
    # Deletar
    delete_response = client.delete(f"/voluntarios/{voluntario_id}")
    assert delete_response.status_code == 204
    
    # Verificar que está inativo (não removido)
    get_response = client.get(f"/voluntarios/{voluntario_id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "inativo"

def test_filtrar_por_status():
    """Deve filtrar voluntários por status"""
    # Criar voluntários
    client.post("/voluntarios", json={
        "nome": "Ativo 1",
        "email": "ativo1@example.com",
        "telefone": "(11) 96666-6666",
        "cargo_pretendido": "Monitor",
        "disponibilidade": "manhã"
    })
    
    response2 = client.post("/voluntarios", json={
        "nome": "Ativo 2",
        "email": "ativo2@example.com",
        "telefone": "(11) 97777-7777",
        "cargo_pretendido": "Instrutor",
        "disponibilidade": "tarde"
    })
    
    # Deletar um (soft delete)
    voluntario_id = response2.json()["id"]
    client.delete(f"/voluntarios/{voluntario_id}")
    
    # Filtrar por status ativo
    response = client.get("/voluntarios?status=ativo")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "ativo"

def test_filtrar_por_cargo():
    """Deve filtrar voluntários por cargo"""
    # Criar voluntários com cargos diferentes
    client.post("/voluntarios", json={
        "nome": "Instrutor 1",
        "email": "instrutor1@example.com",
        "telefone": "(11) 98888-8888",
        "cargo_pretendido": "Instrutor de Yoga",
        "disponibilidade": "manhã"
    })
    
    client.post("/voluntarios", json={
        "nome": "Monitor 1",
        "email": "monitor1@example.com",
        "telefone": "(11) 99999-9999",
        "cargo_pretendido": "Monitor de Informática",
        "disponibilidade": "tarde"
    })
    
    # Filtrar por cargo
    response = client.get("/voluntarios?cargo=instrutor")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "instrutor" in data[0]["cargo_pretendido"].lower()

def test_validacao_campos_obrigatorios():
    """Deve validar campos obrigatórios"""
    # Tentar criar sem nome
    response = client.post("/voluntarios", json={
        "email": "teste@example.com",
        "telefone": "(11) 91111-1111",
        "cargo_pretendido": "Monitor",
        "disponibilidade": "manhã"
    })
    assert response.status_code == 422

def test_validacao_email_invalido():
    """Deve validar formato de email"""
    response = client.post("/voluntarios", json={
        "nome": "Teste",
        "email": "email-invalido",
        "telefone": "(11) 91111-1111",
        "cargo_pretendido": "Monitor",
        "disponibilidade": "manhã"
    })
    assert response.status_code == 422