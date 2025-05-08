from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import database

Base = database.Base

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
    # Permitir NULL para não violar unique em inserts iniciais
    codigo_barras = Column(String(20), unique=True, index=True, nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="produtos")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)

    produtos = relationship("Produto", back_populates="usuario", cascade="all, delete")