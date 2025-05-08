from sqlalchemy.orm import Session
from models import Produto, Usuario
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
import schemas

# Inicializando o contexto de criptografia com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Criar Produto
def criar_produto(db: Session, produto_data: schemas.ProdutoCreate):
    if produto_data.quantidade_total > 0:
        valor_unitario = produto_data.valor_total / produto_data.quantidade_total
    else:
        valor_unitario = 0.0

    valor_imposto = produto_data.valor_total * (produto_data.aliquota_imposto / 100)
    valor_total_com_imposto = produto_data.valor_total + valor_imposto
    valor_venda_un = valor_unitario + (valor_unitario * (produto_data.margem_lucro / 100))

    # Gerar código de barras sequencial se não for informado ou for None
    if not produto_data.codigo_barras or produto_data.codigo_barras == '':
        # Consultar o último código de barras numérico
        ultimo_produto = db.query(Produto).order_by(Produto.codigo_barras.desc()).first()
        
        # Verificar se existe um último produto e o código de barras é numérico
        if ultimo_produto and ultimo_produto.codigo_barras.isdigit():
            novo_codigo_barras = str(int(ultimo_produto.codigo_barras) + 1)
        else:
            novo_codigo_barras = '1'  # Se não houver código de barras, começar de 1
    else:
        novo_codigo_barras = produto_data.codigo_barras

    produto = Produto(
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
        codigo_barras=novo_codigo_barras,
        usuario_id=produto_data.usuario_id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto





# Listar Produtos por Usuário
def listar_produtos(db: Session, usuario_id: int):
    return db.query(Produto).filter(Produto.usuario_id == usuario_id).order_by(Produto.nome_produto.asc()).all()


# Calcular Custos
def calcular_custos(db: Session, produto_id: int, quantidade: int):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
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
def update_produto(db: Session, produto_id: int, produto_data: schemas.ProdutoUpdate):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        return None

    # Atualização de campos opcionais
    if produto_data.nome_produto is not None:
        produto.nome_produto = produto_data.nome_produto
    if produto_data.quantidade_total is not None:
        produto.quantidade_total = produto_data.quantidade_total
    if produto_data.valor_total is not None:
        produto.valor_total = produto_data.valor_total
    if produto_data.margem_lucro is not None:
        produto.margem_lucro = produto_data.margem_lucro
    if produto_data.aliquota_imposto is not None:
        produto.aliquota_imposto = produto_data.aliquota_imposto
    if produto_data.gastos_fixos is not None:
        produto.gastos_fixos = produto_data.gastos_fixos
    if produto_data.codigo_barras is not None:
        produto.codigo_barras = produto_data.codigo_barras

    # Recalcula os campos derivados
    if produto.quantidade_total > 0:
        valor_unitario = produto.valor_total / produto.quantidade_total
    else:
        valor_unitario = 0.0

    valor_imposto = produto.valor_total * (produto.aliquota_imposto / 100)
    valor_total_com_imposto = produto.valor_total + valor_imposto
    valor_venda_un = valor_unitario + (valor_unitario * (produto.margem_lucro / 100))

    produto.valor_unitario = valor_unitario
    produto.valor_imposto = valor_imposto
    produto.valor_total_com_imposto = valor_total_com_imposto
    produto.valor_venda_un = valor_venda_un

    db.commit()
    db.refresh(produto)
    return produto


# Deletar Produto
def delete_produto(db: Session, produto_id: int):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        return None
    db.delete(produto)
    db.commit()
    return produto


# Criar Usuário
def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = pwd_context.hash(usuario.senha)
    db_usuario = Usuario(email=usuario.email, senha=hashed_password)
    
    try:
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        raise ValueError("Este email já está em uso.")


# Autenticar Usuário
def autenticar_usuario(db: Session, usuario: schemas.UsuarioLogin):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario and pwd_context.verify(usuario.senha, db_usuario.senha):
        return db_usuario
    return None

def get_produtos_por_usuario(db: Session, usuario_id: int):
    return db.query(models.Produto).filter(models.Produto.usuario_id == usuario_id).all()
