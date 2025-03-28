# backend/models.py
from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome_produto = Column(String, index=True)
    metrica = Column(String)
    quantidade_total = Column(Integer)
    valor_total = Column(Float)
    valor_unitario = Column(Float)
    margem_lucro = Column(Float)
    valor_venda_un = Column(Float)
    aliquota_imposto = Column(Float)
    valor_imposto = Column(Float)
    valor_total_com_imposto = Column(Float)
