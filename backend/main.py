from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship
from passlib.context import CryptContext
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt

from backend.schemas import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioLoginResponse,
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoOut,
)

# Configuração do banco PostgreSQL
DATABASE_URL = "postgresql://postgres:FGuJhYAVyAtiugBcayNwSqejXyjbjMUv@switchback.proxy.rlwy.net:59685/railway"
engine = create_engine(DATABASE_URL)
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

Base.metadata.create_all(bind=engine)

# Segurança de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(s: str) -> str:
    return pwd_context.hash(s)
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Configuração JWT
SECRET_KEY = "cce12b0244a74f4ba148c1b0d55e128d69e157cb6fbd4373877d0e0609d2fd18"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    exc = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise exc
        return sub
    except JWTError:
        raise exc

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
        raise HTTPException(404, "Usuário não encontrado")
    return user

# Instância FastAPI e CORS (com persistAuthorization)
app = FastAPI(
    swagger_ui_parameters={"persistAuthorization": True}
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints de Usuário
@app.post("/usuarios", response_model=UsuarioLoginResponse, status_code=201)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(400, "Email já cadastrado")
    novo = Usuario(email=usuario.email, senha=hash_password(usuario.senha))
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not user or not verify_password(usuario.senha, user.senha):
        raise HTTPException(401, "Email ou senha inválidos")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Endpoints de Produtos
@app.post("/produtos", response_model=ProdutoOut, status_code=201)
def criar_produto(
    prod: ProdutoCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    unit = prod.valor_total / prod.quantidade_total if prod.quantidade_total > 0 else 0.0
    imp = prod.valor_total * (prod.aliquota_imposto / 100)
    total_imp = prod.valor_total + imp
    venda_unit = unit + (unit * (prod.margem_lucro / 100))

    novo = ProdutoDB(
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
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.get("/produtos", response_model=List[ProdutoOut])
def listar_produtos(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    return db.query(ProdutoDB).filter(ProdutoDB.usuario_id == user.id).all()

@app.put("/produtos/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(
    produto_id: int,
    prod: ProdutoCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    p = db.query(ProdutoDB).get(produto_id)
    if not p or p.usuario_id != user.id:
        raise HTTPException(403, "Acesso negado ou produto não existe")
    for attr in ["nome_produto","quantidade_total","valor_total","margem_lucro",
                 "aliquota_imposto","gastos_fixos","codigo_barras"]:
        setattr(p, attr, getattr(prod, attr))
    p.valor_unitario = p.valor_total / p.quantidade_total if p.quantidade_total > 0 else 0.0
    imp = p.valor_total * (p.aliquota_imposto / 100)
    p.valor_imposto = imp
    p.valor_total_com_imposto = p.valor_total + imp
    p.valor_venda_un = p.valor_unitario + (p.valor_unitario * (p.margem_lucro / 100))
    db.commit()
    db.refresh(p)
    return p

@app.delete("/produtos/{produto_id}", status_code=204)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user)
):
    p = db.query(ProdutoDB).get(produto_id)
    if not p or p.usuario_id != user.id:
        raise HTTPException(403, "Acesso negado ou produto não existe")
    db.delete(p)
    db.commit()
