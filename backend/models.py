from sqlalchemy import Column, Integer, String, Float
import database

Base = database.Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome_produto = Column(String, index=True)
    metrica = Column(String)
    quantidade_total = Column(Integer)
    valor_total = Column(Float)
    valor_unitario = Column(Float)
    margem_lucro = Column(Float, default=0.0)
    valor_venda_un = Column(Float)
    aliquota_imposto = Column(Float, default=0.0)
    valor_imposto = Column(Float)
    valor_total_com_imposto = Column(Float)
    gastos_fixos = Column(Float, default=0.0)
