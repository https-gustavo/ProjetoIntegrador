from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, database, schemas

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas do banco
models.Base.metadata.create_all(bind=database.engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#ROTAS DE PRODUTO

@app.post("/produtos/", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.criar_produto(db, produto)

@app.get("/produtos/", response_model=list[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return crud.listar_produtos(db)

#ROTA: Buscar produto por ID

@app.get("/produtos/{produto_id}", response_model=schemas.Produto)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.get_produto_by_id(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.put("/produtos/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(produto_id: int, produto_update: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    produto = crud.update_produto(db, produto_id, produto_update)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.delete("/produtos/{produto_id}", response_model=schemas.DeleteResponse)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.delete_produto(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": f"Produto '{produto.nome_produto}' deletado com sucesso"}

#ROTA DE LOGIN

@app.post("/login/")
def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    user = crud.autenticar_usuario(db, usuario.email, usuario.senha)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    return {"message": "Login realizado com sucesso", "usuario": user.email}
