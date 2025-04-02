from sqlalchemy.orm import Session
import models

#EndPoint Criar Produto
def criar_produto(db: Session, nome_produto: str, metrica: str, quantidade_total: int, valor_total: float, margem_lucro: float = 0.0, aliquota_imposto: float = 0.0, gastos_fixos: float = 0.0):
    if quantidade_total != 0:
        valor_unitario = valor_total / quantidade_total 
    else:
        valor_unitario = 0.0
    valor_imposto = valor_total * (aliquota_imposto / 100)
    valor_total_com_imposto = valor_total + valor_imposto
    valor_venda_un = valor_unitario + (valor_unitario * (margem_lucro / 100))

    produto = models.Produto(
        nome_produto=nome_produto,
        metrica=metrica,
        quantidade_total=quantidade_total,
        valor_total=valor_total,
        valor_unitario=valor_unitario,
        margem_lucro=margem_lucro,
        valor_venda_un=valor_venda_un,
        aliquota_imposto=aliquota_imposto,
        valor_imposto=valor_imposto,
        valor_total_com_imposto=valor_total_com_imposto,
        gastos_fixos=gastos_fixos
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

#EndPoint Listar Produtos 
def listar_produtos(db: Session):
    return db.query(models.Produto).order_by(models.Produto.nome_produto.asc()).all()

#EndPoint Calculo Custos
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