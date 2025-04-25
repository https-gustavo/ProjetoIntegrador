import React, { useState } from 'react';

const API_URL = 'http://localhost:8000';

function ListaProdutos({ produtos, onEditar, onNovoProduto, atualizarProdutos }) {
  const [termoBusca, setTermoBusca] = useState('');

  const formatarMoeda = valor =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(valor);

  const excluirProduto = async id => {
    if (!window.confirm('Deseja excluir este produto?')) return;
    try {
      await fetch(`${API_URL}/produtos/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${JSON.parse(localStorage.getItem('auth')).access_token}`
        }
      });
      atualizarProdutos();
    } catch (error) {
      console.error('Erro ao excluir produto:', error);
    }
  };

  const calcularValorVenda = produto => {
    const quantidade = produto.quantidade_total || 1;
    const custoUnitario = produto.valor_total / quantidade;
    const imposto = custoUnitario * (produto.aliquota_imposto / 100);
    const gastosFixos = custoUnitario * (produto.gastos_fixos / 100);
    const lucro = custoUnitario * (produto.margem_lucro / 100);
    return custoUnitario + imposto + gastosFixos + lucro;
  };

  const produtosFiltrados = produtos.filter(p =>
    (p.nome_produto || '').toLowerCase().includes(termoBusca.toLowerCase()) ||
    (p.codigo_barras || '').toLowerCase().includes(termoBusca.toLowerCase())
  );

  return (
    <div style={container}>
      <h2 style={titulo}> Lista de Produtos</h2>

      <div style={filtros}>
        <div style={buscaWrapper}>
          <span style={iconeBusca}>🔍</span>
          <input
            type="text"
            placeholder="Buscar por nome ou código de barras..."
            value={termoBusca}
            onChange={e => setTermoBusca(e.target.value)}
            style={inputBusca}
          />
        </div>

        <button onClick={onNovoProduto} style={botaoCadastro}>
          + Cadastrar Produto
        </button>
      </div>

      <table style={tabela}>
        <thead>
          <tr style={cabecalho}>
            {[
              'Código de Barras',
              'Nome',
              'Qtd',
              'Valor Total',
              'Unitário',
              'Imposto (%)',
              'Fixos (%)',
              'Lucro (%)',
              'Venda',
              'Ações',
            ].map(col => (
              <th key={col} style={th}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {produtosFiltrados.map((p, i) => (
            <tr key={p.id} style={i % 2 === 0 ? linhaPar : linhaImpar}>
              <td style={td}>{p.codigo_barras}</td>
              <td style={td}>{p.nome_produto}</td>
              <td style={td}>{p.quantidade_total}</td>
              <td style={td}>{formatarMoeda(p.valor_total)}</td>
              <td style={td}>{formatarMoeda(p.valor_total / (p.quantidade_total || 1))}</td>
              <td style={td}>{p.aliquota_imposto}%</td>
              <td style={td}>{p.gastos_fixos}%</td>
              <td style={td}>{p.margem_lucro}%</td>
              <td style={td}>{formatarMoeda(calcularValorVenda(p))}</td>
              <td style={{ ...td, textAlign: 'center' }}>
                <button onClick={() => onEditar(p)} style={editBtn}>✏️</button>
                <button onClick={() => excluirProduto(p.id)} style={deleteBtn}>🗑️</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const container = {
  maxWidth: '1100px',
  margin: '2rem auto',
  padding: '1.5rem',
  backgroundColor: '#f9f9f9',
  borderRadius: '12px',
  boxShadow: '0 0 10px rgba(0,0,0,0.1)',
};

const titulo = {
  textAlign: 'center',
  marginBottom: '1.5rem',
  fontSize: '1.8rem',
};

const filtros = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  flexWrap: 'wrap',
  gap: '1rem',
  marginBottom: '1rem',
};

const buscaWrapper = {
  position: 'relative',
  flex: '1 1 250px',
  maxWidth: '300px',
};

const iconeBusca = {
  position: 'absolute',
  top: '50%',
  left: '10px',
  transform: 'translateY(-50%)',
  color: '#888',
  pointerEvents: 'none',
  fontSize: '18px',
};

const inputBusca = {
  padding: '8px 8px 8px 32px',
  borderRadius: '15px',
  border: '1px solid #ccc',
  width: '100%',
  fontSize: '14px',
  outline: 'none',
};

const botaoCadastro = {
  padding: '8px 16px',
  backgroundColor: '#4CAF50',
  color: 'white',
  border: 'none',
  borderRadius: '15px',
  cursor: 'pointer',
  fontWeight: 'bold',
  height: '40px',
  whiteSpace: 'nowrap',
};

const tabela = {
  width: '100%',
  borderCollapse: 'collapse',
  backgroundColor: 'white',
  borderRadius: '10px',
  overflow: 'hidden',
};

const cabecalho = {
  backgroundColor: '#f0f0f0',
  color: '#333',
};

const th = {
  padding: '10px',
  textAlign: 'left',
  fontWeight: 'bold',
  borderBottom: '2px solid #ddd',
};

const td = {
  padding: '10px',
  fontSize: '14px',
  verticalAlign: 'middle',
};

const linhaPar = {
  backgroundColor: '#fff',
  borderBottom: '1px solid #ddd',
};

const linhaImpar = {
  backgroundColor: '#fafafa',
  borderBottom: '1px solid #ddd',
};

const editBtn = {
  padding: '6px 10px',
  marginRight: '6px',
  backgroundColor: '#2196F3',
  color: 'white',
  border: 'none',
  borderRadius: '15px',
  cursor: 'pointer',
};

const deleteBtn = {
  padding: '6px 10px',
  backgroundColor: '#f44336',
  color: 'white',
  border: 'none',
  borderRadius: '15px',
  cursor: 'pointer',
};

export default ListaProdutos;
