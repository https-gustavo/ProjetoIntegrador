from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

# -----------------------------
# PRODUTOS
# -----------------------------

def criar_produto(db: Session, produto_data: schemas.ProdutoCreate):
    if produto_data.quantidade_total > 0:
        valor_unitario = produto_data.valor_total / produto_data.quantidade_total
    else:
        valor_unitario = 0.0

    valor_imposto = valor_unitario * (produto_data.aliquota_imposto / 100)
    gastos = valor_unitario * (produto_data.gastos_fixos / 100) if produto_data.gastos_fixos else 0
    lucro = valor_unitario * (produto_data.margem_lucro / 100)

    valor_venda_un = valor_unitario + valor_imposto + gastos + lucro
    valor_total_com_imposto = produto_data.valor_total + (produto_data.valor_total * (produto_data.aliquota_imposto / 100))

    produto = models.Produto(
        nome_produto=produto_data.nome_produto,
        metrica=produto_data.metrica,
        quantidade_total=produto_data.quantidade_total,
        valor_total=produto_data.valor_total,
        valor_unitario=valor_unitario,
        margem_lucro=produto_data.margem_lucro,
        valor_venda_un=valor_venda_un,
        aliquota_imposto=produto_data.aliquota_imposto,
        valor_imposto=valor_imposto,
        valor_total_com_imposto=valor_total_com_imposto,
        gastos_fixos=produto_data.gastos_fixos
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

def listar_produtos(db: Session):
    return db.query(models.Produto).order_by(models.Produto.nome_produto.asc()).all()

def calcular_custos(db: Session, produto_id: int, quantidade: int) -> schemas.CalculoCustoResponse:
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    custo_total = produto.valor_unitario * quantidade
    lucro = custo_total * (produto.margem_lucro / 100)
    imposto = custo_total * (produto.aliquota_imposto / 100)
    custo_com_imposto = custo_total + imposto

    return schemas.CalculoCustoResponse(
        produto=produto.nome_produto,
        quantidade=quantidade,
        custo_total=custo_total,
        lucro=lucro,
        imposto=imposto,
        custo_com_imposto=custo_com_imposto
    )

def get_produto_by_id(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()

def update_produto(db: Session, produto_id: int, produto_update: schemas.ProdutoUpdate):
    # Busca o produto no banco
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        return None

    # Atualiza somente os campos enviados no request
    for key, value in produto_update.dict(exclude_unset=True).items():
        setattr(produto, key, value)

    # Evita divisão por zero
    if produto.quantidade_total > 0:
        produto.valor_unitario = produto.valor_total / produto.quantidade_total
    else:
        produto.valor_unitario = 0.0

    # Calcula valores derivados
    produto.valor_imposto = produto.valor_unitario * (produto.aliquota_imposto / 100)

    gastos = produto.valor_unitario * (produto.gastos_fixos / 100) if produto.gastos_fixos else 0
    lucro = produto.valor_unitario * (produto.margem_lucro / 100)

    produto.valor_venda_un = produto.valor_unitario + produto.valor_imposto + gastos + lucro
    produto.valor_total_com_imposto = produto.valor_total + (produto.valor_total * (produto.aliquota_imposto / 100))

    # LOG para debug
    print("----- DADOS CALCULADOS -----")
    print("Produto ID:", produto_id)
    print("Valor unitário:", produto.valor_unitario)
    print("Valor imposto:", produto.valor_imposto)
    print("Gastos fixos (reais):", gastos)
    print("Lucro (reais):", lucro)
    print("Valor de venda sugerido:", produto.valor_venda_un)
    print("Valor total com imposto:", produto.valor_total_com_imposto)
    print("----------------------------")

    # Commit no banco e retorna produto atualizado
    db.commit()
    db.refresh(produto)
    return produto


def delete_produto(db: Session, produto_id: int):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        return None

    db.delete(produto)
    db.commit()
    return produto

# -----------------------------
# USUÁRIO
# -----------------------------

def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not usuario or usuario.senha != senha:
        return None
    return usuario
