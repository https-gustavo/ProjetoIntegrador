# criar_tabelas.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Pega a DATABASE_URL do Railway
DATABASE_URL = os.getenv("DATABASE_URL")

# Configura o engine
engine = create_engine(DATABASE_URL)

# Define a Base
Base = declarative_base()

# Define seus modelos de tabelas aqui

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)

    produtos = relationship("Produto", back_populates="usuario", cascade="all, delete")

class Produto(Base):
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

print("✅ Tabelas criadas com sucesso!")
