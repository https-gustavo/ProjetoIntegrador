from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship
from passlib.context import CryptContext
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

from backend.schemas import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioLoginResponse,
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoOut,
)

# Carrega variáveis de ambiente
load_dotenv()
print("Conexão com banco:", os.getenv("DATABASE_URL"))  # Apenas para debug

# Configuração do banco PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada corretamente no .env")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos SQLAlchemy
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    produtos = relationship("ProdutoDB", back_populates="usuario")

class ProdutoDB(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome_produto = Column(String, index=True, nullable=False)
    quantidade_total = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)
    valor_unitario = Column(Float, nullable=False, default=0.0)
    margem_lucro = Column(Float, default=0.0)
    valor_venda_un = Column(Float, nullable=False, default=0.0)
    aliquota_imposto = Column(Float, default=0.0)
    valor_imposto = Column(Float, nullable=False, default=0.0)
    valor_total_com_imposto = Column(Float, nullable=False, default=0.0)
    gastos_fixos = Column(Float, default=0.0)
    codigo_barras = Column(String(13), unique=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="produtos")

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Segurança de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Configurações do JWT
SECRET_KEY = "cce12b0244a74f4ba148c1b0d55e128d69e157cb6fbd4373877d0e0609d2fd18"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        return sub
    except JWTError:
        raise credentials_exception

# Dependências FastAPI
bearer = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    token = creds.credentials
    email = verify_token(token)
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Instância FastAPI
app = FastAPI(swagger_ui_parameters={"persistAuthorization": True})

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.post("/usuarios", response_model=UsuarioLoginResponse, status_code=201)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    novo_usuario = Usuario(email=usuario.email, senha=hash_password(usuario.senha))
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not user or not verify_password(usuario.senha, user.senha):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/produtos", response_model=ProdutoOut, status_code=201)
def criar_produto(prod: ProdutoCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    unit = prod.valor_total / prod.quantidade_total if prod.quantidade_total > 0 else 0.0
    imp = prod.valor_total * (prod.aliquota_imposto / 100)
    total_imp = prod.valor_total + imp
    venda_unit = unit + (unit * (prod.margem_lucro / 100))

    novo_produto = ProdutoDB(
        nome_produto=prod.nome_produto,
        quantidade_total=prod.quantidade_total,
        valor_total=prod.valor_total,
        valor_unitario=unit,
        margem_lucro=prod.margem_lucro,
        valor_venda_un=venda_unit,
        aliquota_imposto=prod.aliquota_imposto,
        valor_imposto=imp,
        valor_total_com_imposto=total_imp,
        gastos_fixos=prod.gastos_fixos,
        codigo_barras=prod.codigo_barras,
        usuario_id=user.id
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.get("/produtos", response_model=List[ProdutoOut])
def listar_produtos(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return db.query(ProdutoDB).filter(ProdutoDB.usuario_id == user.id).all()

@app.put("/produtos/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(
    produto_id: int,
    prod: ProdutoCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    produto = db.query(ProdutoDB).get(produto_id)
    if not produto or produto.usuario_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado ou produto não existe")

    for attr in ["nome_produto", "quantidade_total", "valor_total", "margem_lucro", "aliquota_imposto", "gastos_fixos", "codigo_barras"]:
        setattr(produto, attr, getattr(prod, attr))

    produto.valor_unitario = produto.valor_total / produto.quantidade_total if produto.quantidade_total > 0 else 0.0
    imp = produto.valor_total * (produto.aliquota_imposto / 100)
    produto.valor_imposto = imp
    produto.valor_total_com_imposto = produto.valor_total + imp
    produto.valor_venda_un = produto.valor_unitario + (produto.valor_unitario * (produto.margem_lucro / 100))

    db.commit()
    db.refresh(produto)
    return produto

@app.delete("/produtos/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    produto = db.query(ProdutoDB).get(produto_id)
    if not produto or produto.usuario_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado ou produto não existe")
    db.delete(produto)
    db.commit()
