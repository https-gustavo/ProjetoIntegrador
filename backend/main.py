from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend import crud, models, database

# Criação das tabelas, caso não existam
models.Base.metadata.create_all(bind=database.engine)

# Inicialização do aplicativo FastAPI
app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar um novo produto
@app.post("/produtos/")
def criar_produto(nome_produto: str, metrica: str, quantidade_total: int, valor_total: float, valor_unitario: float, margem_lucro: float, valor_venda_un: float, aliquota_imposto: float, valor_imposto: float, valor_total_com_imposto: float, db: Session = Depends(get_db)):
    return crud.criar_produto(db, nome_produto, metrica, quantidade_total, valor_total, valor_unitario, margem_lucro, valor_venda_un, aliquota_imposto, valor_imposto, valor_total_com_imposto)
