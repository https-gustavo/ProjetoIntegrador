from pydantic import BaseModel
from typing import Optional, List

# --- Usuário ---
class UsuarioCreate(BaseModel):
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioLoginResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# --- Produto ---
class ProdutoCreate(BaseModel):
    nome_produto: str
    quantidade_total: int
    valor_total: float
    margem_lucro: Optional[float] = 0.0
    aliquota_imposto: Optional[float] = 0.0
    gastos_fixos: Optional[float] = 0.0
    codigo_barras: str
    # usuario_id removido corretamente

class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = None
    quantidade_total: Optional[int] = None
    valor_total: Optional[float] = None
    margem_lucro: Optional[float] = None
    aliquota_imposto: Optional[float] = None
    gastos_fixos: Optional[float] = None
    codigo_barras: Optional[str] = None

class ProdutoOut(BaseModel):
    id: int
    nome_produto: str
    quantidade_total: int
    valor_total: float
    valor_unitario: float
    margem_lucro: float
    valor_venda_un: float
    aliquota_imposto: float
    valor_imposto: float
    valor_total_com_imposto: float
    gastos_fixos: float
    codigo_barras: str
    usuario_id: int

    class Config:
        from_attributes = True
