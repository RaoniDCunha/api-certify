# 🎯 API de Gerenciamento de Voluntários

Sistema CRUD (Create, Read, Update, Delete) para cadastro e gerenciamento de voluntários usando FastAPI.

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **Poetry** - Gerenciamento de dependências
- **Pytest** - Testes automatizados

## 📋 Requisitos

- Python 3.10 ou superior
- Poetry instalado

### Instalar Poetry

```bash
# Linux/macOS/WSL
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## 🔧 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd api-certify
```

### 2. Instalar Dependências com Poetry

```bash
# Instalar todas as dependências
poetry install

# Ativar ambiente virtual
poetry shell
```

### 3. Verificar Instalação

```bash
# Verificar versão do Python no ambiente Poetry
poetry run python --version

# Listar dependências instaladas
poetry show
```

## ▶️ Como Executar

### Opção 1: Com Poetry Run

```bash
poetry run uvicorn main:app --reload
```

### Opção 2: Dentro do Shell do Poetry

```bash
# Ativar shell
poetry shell

# Executar aplicação
uvicorn main:app --reload
```

### Opção 3: Executar Diretamente

```bash
python main.py
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação Interativa

Acesse a documentação automática do Swagger:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Executar Testes

```bash
# Com Poetry Run
poetry run pytest test_main.py -v

# Ou dentro do shell
poetry shell
pytest test_main.py -v

# Com cobertura de código
poetry run pytest test_main.py -v --cov=main
```

## 📋 Endpoints Disponíveis

### 1. **POST /voluntarios** - Cadastrar Voluntário

**Request:**
```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "(11) 98765-4321",
  "cargo_pretendido": "Instrutor",
  "disponibilidade": "manhã"
}
```

**Response (201):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "(11) 98765-4321",
  "cargo_pretendido": "Instrutor",
  "disponibilidade": "manhã",
  "status": "ativo",
  "data_inscricao": "2024-01-15T10:30:00"
}
```

### 2. **GET /voluntarios** - Listar Voluntários

**Filtros disponíveis (query params):**
- `status`: ativo, inativo, pendente
- `cargo`: texto parcial do cargo
- `disponibilidade`: manhã, tarde, noite, finais de semana, integral

**Exemplos:**
```bash
# Listar todos
GET /voluntarios

# Filtrar por status
GET /voluntarios?status=ativo

# Filtrar por cargo
GET /voluntarios?cargo=instrutor

# Filtrar por disponibilidade
GET /voluntarios?disponibilidade=manhã

# Múltiplos filtros
GET /voluntarios?status=ativo&cargo=monitor
```

### 3. **GET /voluntarios/{id}** - Buscar Voluntário

**Response (200):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "(11) 98765-4321",
  "cargo_pretendido": "Instrutor",
  "disponibilidade": "manhã",
  "status": "ativo",
  "data_inscricao": "2024-01-15T10:30:00"
}
```

### 4. **PUT /voluntarios/{id}** - Atualizar Voluntário

**Request (campos opcionais):**
```json
{
  "nome": "João Silva Santos",
  "telefone": "(11) 91234-5678",
  "cargo_pretendido": "Coordenador",
  "disponibilidade": "tarde",
  "status": "ativo"
}
```

### 5. **DELETE /voluntarios/{id}** - Deletar Voluntário

Soft delete: marca como inativo ao invés de remover

**Response (204):** No Content

## ✅ Funcionalidades Implementadas

### Obrigatórias
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Validação de email único
- ✅ Campos obrigatórios validados
- ✅ Soft delete (marca como inativo)
- ✅ Data de inscrição automática
- ✅ Gerenciamento com Poetry

### Diferenciais
- ✅ Filtros por status, cargo e disponibilidade
- ✅ Tratamento de erros (404, 409, 422)
- ✅ 10+ testes implementados
- ✅ Documentação automática Swagger
- ✅ Uso de Enums para validação
- ✅ Validação de email com Pydantic

## 🎨 Estrutura de Dados

### Disponibilidade (Enum)
- `manhã`
- `tarde`
- `noite`
- `finais de semana`
- `integral`

### Status (Enum)
- `ativo`
- `inativo`
- `pendente`

### Modelo Voluntário
```python
{
  "id": int,
  "nome": str (3-100 caracteres),
  "email": EmailStr (único),
  "telefone": str (mínimo 10 caracteres),
  "cargo_pretendido": str (mínimo 3 caracteres),
  "disponibilidade": DisponibilidadeEnum,
  "status": StatusEnum,
  "data_inscricao": datetime
}
```

## 🔒 Validações Implementadas

1. **Email único**: Não permite cadastro duplicado
2. **Campos obrigatórios**: nome, email, telefone, cargo_pretendido, disponibilidade
3. **Tamanho mínimo**: nome (3 chars), cargo (3 chars), telefone (10 chars)
4. **Formato de email**: Validado pelo Pydantic
5. **Enums**: Valores fixos para disponibilidade e status

## ⚠️ Tratamento de Erros

- **404 Not Found**: Voluntário não encontrado
- **409 Conflict**: Email já cadastrado
- **422 Unprocessable Entity**: Dados inválidos

## 💡 Decisões Técnicas

### 1. Fake Database em Memória
- **Por quê?** Simplicidade para demonstração
- **Vantagem:** Não requer configuração de banco
- **Limitação:** Dados são perdidos ao reiniciar

### 2. Soft Delete
- **Por quê?** Preservar histórico
- **Como:** Marca status como "inativo"
- **Vantagem:** Auditoria e recuperação de dados

### 3. Validação com Pydantic
- **EmailStr:** Valida formato de email
- **Field:** Define validações (min/max length)
- **Enums:** Garante valores permitidos

### 4. Poetry para Dependências
- **Por quê?** Gerenciamento moderno e isolado
- **Vantagens:** 
  - Lock de versões
  - Ambiente virtual automático
  - Resolução de dependências

## 🐛 Troubleshooting

### Erro: "Poetry command not found"
```bash
# Adicionar Poetry ao PATH ou reinstalar
curl -sSL https://install.python-poetry.org | python3 -
```

### Erro ao instalar dependências
```bash
# Limpar cache e reinstalar
poetry cache clear pypi --all
poetry install
```

### Porta 8000 já em uso
```bash
# Usar outra porta
poetry run uvicorn main:app --reload --port 8001
```

## 📦 Dependências do Projeto

### Principais
- `fastapi ^0.115.0` - Framework web
- `uvicorn[standard] ^0.32.0` - Servidor ASGI
- `pydantic[email] ^2.9.0` - Validação de dados
- `email-validator ^2.2.0` - Validação de email

### Desenvolvimento
- `pytest ^8.3.0` - Testes
- `httpx ^0.27.0` - Cliente HTTP para testes

## 📝 Comandos Úteis

```bash
# Adicionar nova dependência
poetry add nome-do-pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev nome-do-pacote

# Atualizar dependências
poetry update

# Mostrar dependências instaladas
poetry show

# Verificar vulnerabilidades
poetry check

# Exportar requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

## 🤝 Como Contribuir

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

## 👤 Autor

**Seu Nome**
- Email: seu.email@example.com
- GitHub: [@seuusuario](https://github.com/seuusuario)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!