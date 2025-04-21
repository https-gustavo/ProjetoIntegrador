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
        quantidade_total=produto_data.quantidade_total,
        valor_total=produto_data.valor_total,
        valor_unitario=valor_unitario,
        margem_lucro=produto_data.margem_lucro,
        valor_venda_un=valor_venda_un,
        aliquota_imposto=produto_data.aliquota_imposto,
        valor_imposto=valor_imposto,
        valor_total_com_imposto=valor_total_com_imposto,
        gastos_fixos=produto_data.gastos_fixos,
        codigo_barras=produto_data.codigo_barras  # Incluindo código de barras
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
            "codigo_barras": produto.codigo_barras,  # Incluindo código de barras
            "quantidade": quantidade,
            "custo_total": custo_total,
            "lucro": lucro,
            "imposto": imposto,
            "custo_com_imposto": custo_com_imposto
        }
    return {"erro": "Produto não encontrado"}

# Atualizar Produto
def update_produto(db: Session, produto_id: int, produto_data: schemas.ProdutoCreate):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        return None

    if produto_data.quantidade_total > 0:
        valor_unitario = produto_data.valor_total / produto_data.quantidade_total
    else:
        valor_unitario = 0.0

    valor_imposto = produto_data.valor_total * (produto_data.aliquota_imposto / 100)
    valor_total_com_imposto = produto_data.valor_total + valor_imposto
    valor_venda_un = valor_unitario + (valor_unitario * (produto_data.margem_lucro / 100))

    produto.nome_produto = produto_data.nome_produto
    produto.quantidade_total = produto_data.quantidade_total
    produto.valor_total = produto_data.valor_total
    produto.valor_unitario = valor_unitario
    produto.margem_lucro = produto_data.margem_lucro
    produto.valor_venda_un = valor_venda_un
    produto.aliquota_imposto = produto_data.aliquota_imposto
    produto.valor_imposto = valor_imposto
    produto.valor_total_com_imposto = valor_total_com_imposto
    produto.gastos_fixos = produto_data.gastos_fixos
    produto.codigo_barras = produto_data.codigo_barras

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


