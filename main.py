from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, database, schemas

app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criar Produto
@app.post("/produtos/", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.criar_produto(db, produto)

# Listar Produtos
@app.get("/produtos/", response_model=list[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return crud.listar_produtos(db)

# Calcular Custos
@app.post("/calculos/", response_model=schemas.CalculoCustoResponse)
def calcular_custos(produto_id: int, quantidade: int, db: Session = Depends(get_db)):
    return crud.calcular_custos(db, produto_id, quantidade)


# Atualizar Produto
@app.put("/produtos/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(produto_id: int, produto_update: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    produto = crud.atualizar_produto(db, produto_id, produto_update)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Deletar Produto
@app.delete("/produtos/{produto_id}", response_model=schemas.DeleteResponse)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.delete_produto(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso"}
