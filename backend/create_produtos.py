from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models  # Importar os modelos, incluindo Produto

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:teste@localhost:8280/calculadora_custos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Criar um produto para adicionar ao banco
produto = models.Produto(
    nome_produto="Produto Teste",
    metrica="kg",
    quantidade_total=100,
    valor_total=500,
    valor_unitario=5,
    margem_lucro=0.2,
    valor_venda_un=6,
    aliquota_imposto=0.15,
    valor_imposto=75,
    valor_total_com_imposto=575,
    gastos_fixos=50
)

session.add(produto)
session.commit()
session.close()
