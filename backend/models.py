from sqlalchemy import Column, Integer, String, Float
import database

Base = database.Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome_produto = Column(String, index=True, nullable=False)
    metrica = Column(String, nullable=False)
    quantidade_total = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)
    valor_unitario = Column(Float, nullable=False, default=0.0)
    margem_lucro = Column(Float, default=0.0)
    valor_venda_un = Column(Float, nullable=False, default=0.0)
    aliquota_imposto = Column(Float, default=0.0)
    valor_imposto = Column(Float, nullable=False, default=0.0)
    valor_total_com_imposto = Column(Float, nullable=False, default=0.0)
    gastos_fixos = Column(Float, default=0.0)
