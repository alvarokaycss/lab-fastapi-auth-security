# 🔐 Lab FastAPI - Auth & Security

API RESTful desenvolvida com FastAPI implementando autenticação JWT, autorização e operações CRUD para gerenciamento de usuários e artigos.

## 🚀 Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM com suporte assíncrono
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados (via asyncpg)
- **[JWT](https://jwt.io/)** - Autenticação via tokens
- **[Bcrypt](https://pypi.org/project/bcrypt/)** - Hashing de senhas
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI

## 📁 Estrutura do Projeto

```
lab-fastapi-auth-security/
├── api/
│   └── v1/
│       ├── api.py                 # Router principal da API v1
│       └── endpoints/
│           ├── artigo.py          # Endpoints de artigos
│           └── usuario.py         # Endpoints de usuários
├── core/
│   ├── auth.py                    # Lógica de autenticação JWT
│   ├── database.py                # Configuração do banco de dados
│   ├── deps.py                    # Dependências (sessão DB, usuário atual)
│   ├── security.py                # Funções de segurança (hash, verify)
│   └── settings.py                # Configurações da aplicação
├── models/
│   ├── __all_models.py            # Importação de todos os modelos
│   ├── artigo_models.py           # Modelo de Artigo
│   └── usuario_models.py          # Modelo de Usuário
├── schemas/
│   ├── artigo_schema.py           # Schemas Pydantic de Artigo
│   └── usuario_schema.py          # Schemas Pydantic de Usuário
├── .env                           # Variáveis de ambiente (não versionado)
├── .gitignore
├── criar_tabelas.py               # Script para criar tabelas no banco
├── main.py                        # Entry point da aplicação
└── requirements.txt               # Dependências do projeto
```

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd lab-fastapi-auth-security
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Banco de Dados
DB_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco

# Servidor
PORT=8000

# JWT Secret (gere um token seguro)
JWT_SECRET=seu_token_secreto_aqui
```

> **💡 Dica:** Para gerar um `JWT_SECRET` seguro, execute:
> ```python
> import secrets
> print(secrets.token_urlsafe(32))
> ```

### 6. Crie as tabelas no banco de dados

```bash
python criar_tabelas.py
```

> ⚠️ **Atenção:** Este comando apaga todas as tabelas existentes e as recria.

## 🏃 Executando a Aplicação

### Modo de desenvolvimento (com reload automático)

```bash
python main.py
```

Ou use o Uvicorn diretamente:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

A API estará disponível em: `http://127.0.0.1:8000`

### Documentação Interativa

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 📚 Endpoints da API

### Usuários

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `POST` | `/api/v1/usuarios/signup` | Criar novo usuário | ❌ |
| `POST` | `/api/v1/usuarios/login` | Login (retorna JWT token) | ❌ |
| `GET` | `/api/v1/usuarios/logado` | Dados do usuário autenticado | ✅ |
| `GET` | `/api/v1/usuarios/` | Listar todos os usuários | ❌ |
| `GET` | `/api/v1/usuarios/{id}` | Buscar usuário por ID | ❌ |
| `PUT` | `/api/v1/usuarios/{id}` | Atualizar usuário | ❌ |
| `DELETE` | `/api/v1/usuarios/{id}` | Deletar usuário | ❌ |

### Artigos

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/api/v1/artigos/` | Listar todos os artigos | ❌ |
| `GET` | `/api/v1/artigos/{id}` | Buscar artigo por ID | ❌ |
| `POST` | `/api/v1/artigos/` | Criar novo artigo | ✅ |
| `PUT` | `/api/v1/artigos/{id}` | Atualizar artigo (apenas criador) | ✅ |
| `DELETE` | `/api/v1/artigos/{id}` | Deletar artigo (apenas criador) | ✅ |

## 🔑 Autenticação

### 1. Criar um usuário

```bash
POST /api/v1/usuarios/signup
Content-Type: application/json

{
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@email.com",
  "senha": "senha123",
  "admin": false
}
```

### 2. Fazer login

```bash
POST /api/v1/usuarios/login
Content-Type: application/x-www-form-urlencoded

username=joao@email.com&password=senha123
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Usar o token nas requisições

Adicione o header `Authorization` com o token:

```bash
GET /api/v1/usuarios/logado
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📝 Exemplos de Uso

### Criar um artigo (autenticado)

```bash
POST /api/v1/artigos/
Authorization: Bearer <seu_token>
Content-Type: application/json

{
  "titulo": "Introdução ao FastAPI",
  "descricao": "Um guia completo sobre FastAPI",
  "url_fonte": "https://exemplo.com/artigo"
}
```

### Listar artigos de um usuário

```bash
GET /api/v1/usuarios/1
```

**Resposta:**
```json
{
  "id_usuario": 1,
  "nome": "João",
  "sobrenome": "Silva",
  "email": "joao@email.com",
  "admin": false,
  "artigos": [
    {
      "id_artigo": 1,
      "titulo": "Introdução ao FastAPI",
      "descricao": "Um guia completo sobre FastAPI",
      "url_fonte": "https://exemplo.com/artigo",
      "id_usuario": 1
    }
  ]
}
```

## 🔒 Recursos de Segurança

- ✅ **Hashing de senhas** com Bcrypt
- ✅ **Autenticação JWT** com tokens de 7 dias de validade
- ✅ **Validação de dados** com Pydantic
- ✅ **Proteção de rotas** com dependências do FastAPI
- ✅ **Autorização** - apenas criadores podem editar/deletar seus artigos
- ✅ **Async/Await** - performance com operações assíncronas

## 🗄️ Modelos de Dados

### UsuarioModel

```python
id_usuario: int (PK)
nome: str
sobrenome: str
email: str (unique, indexed)
senha: str (hashed)
admin: bool
artigos: List[ArtigoModel] (relationship)
```

### ArtigoModel

```python
id_artigo: int (PK)
titulo: str
descricao: str
url_fonte: str (HttpUrl)
id_usuario: int (FK)
criador: UsuarioModel (relationship)
```

## 🛠️ Desenvolvimento

### Executar com hot-reload

```bash
uvicorn main:app --reload
```

### Recriar tabelas do banco

```bash
python criar_tabelas.py
```

## 📦 Dependências Principais

```
fastapi==0.128.5
uvicorn==0.40.0
sqlalchemy==2.0.46
asyncpg==0.31.0
pydantic==2.12.5
pydantic-settings==2.7.1
python-jose==3.5.0
passlib==1.7.4
bcrypt==4.1.3
python-multipart==0.0.22
email-validator==2.3.0
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: minha nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é um laboratório de estudo sobre FastAPI, autenticação e segurança.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

⭐ **Desenvolvido com FastAPI** | 🔐 **Auth & Security Lab**
