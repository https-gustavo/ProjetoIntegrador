from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, database

app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#EndPoint Criar Produtos
@app.post("/produtos/")
def criar_produto(nome_produto: str, metrica: str, quantidade_total: int, valor_total: float, margem_lucro: float = 0.0, aliquota_imposto: float = 0.0, gastos_fixos: float = 0.0, db: Session = Depends(get_db)):
    return crud.criar_produto(db, nome_produto, metrica, quantidade_total, valor_total, margem_lucro, aliquota_imposto, gastos_fixos)

#EndPoint Listar Produtos
@app.get("/produtos/")
def listar_produtos(db: Session = Depends(get_db)):
    produtos = crud.listar_produtos(db)
    return produtos

#EndPoint Calculo Custo
@app.post("/calculos/")
def calcular_custos(
        produto_id: int,
        quantidade: int,
        db: Session = Depends(get_db)
):
    return crud.calcular_custos(db, produto_id, quantidade)




