from sqlalchemy.orm import Session
import models, schemas

# Criar Produto
def criar_produto(db: Session, produto_data: schemas.ProdutoCreate):
    if produto_data.quantidade_total > 0:
        valor_unitario = produto_data.valor_total / produto_data.quantidade_total
    else:
        valor_unitario = 0.0

    valor_imposto = produto_data.valor_total * (produto_data.aliquota_imposto / 100)
    valor_total_com_imposto = produto_data.valor_total + valor_imposto
    valor_venda_un = valor_unitario + (valor_unitario * (produto_data.margem_lucro / 100))

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

# Listar Produtos
def listar_produtos(db: Session):
    return db.query(models.Produto).order_by(models.Produto.nome_produto.asc()).all()

# Calcular Custos
def calcular_custos(db: Session, produto_id: int, quantidade: int):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if produto:
        custo_total = produto.valor_unitario * quantidade
        lucro = custo_total * (produto.margem_lucro / 100)
        imposto = custo_total * (produto.aliquota_imposto / 100)
        custo_com_imposto = custo_total + imposto
        return {
            "produto": produto.nome_produto,
            "quantidade": quantidade,
            "custo_total": custo_total,
            "lucro": lucro,
            "imposto": imposto,
            "custo_com_imposto": custo_com_imposto
        }
    return {"erro": "Produto não encontrado"}

# Atualizar Produto
def update_produto(db: Session, produto_id: int, produto_update: schemas.ProdutoUpdate):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        return None

    for key, value in produto_update.dict(exclude_unset=True).items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)
    return produto

# Deletar Produto
def delete_produto(db: Session, produto_id: int):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        return None

    db.delete(produto)
    db.commit()
    return produto
