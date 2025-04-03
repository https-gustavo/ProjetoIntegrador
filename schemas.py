from pydantic import BaseModel
from typing import Optional

# Esquema para Criar Produto
class ProdutoCreate(BaseModel):
    nome_produto: str
    metrica: str
    quantidade_total: int
    valor_total: float
    margem_lucro: Optional[float] = 0.0
    aliquota_imposto: Optional[float] = 0.0
    gastos_fixos: Optional[float] = 0.0

# Esquema para Atualizar Produto
class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = None
    metrica: Optional[str] = None
    quantidade_total: Optional[int] = None
    valor_total: Optional[float] = None
    margem_lucro: Optional[float] = None
    aliquota_imposto: Optional[float] = None
    gastos_fixos: Optional[float] = None

# Esquema para Retorno de Produto
class Produto(ProdutoCreate):
    id: int
    valor_unitario: float
    valor_venda_un: float
    valor_imposto: float
    valor_total_com_imposto: float

    class Config:
        from_attributes = True  # Correção para Pydantic V2

# Esquema para Retorno do Cálculo de Custos
class CalculoCustoResponse(BaseModel):
    produto: str
    quantidade: int
    custo_total: float
    lucro: float
    imposto: float
    custo_com_imposto: float

    class Config:
        from_attributes = True  # Correção para Pydantic V2

# Esquema para Retorno ao Deletar um Produto
class DeleteResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True  # Correção para Pydantic V2
