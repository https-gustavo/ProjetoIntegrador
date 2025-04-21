import React, { useState } from 'react';

function ListaProdutos({ produtos, onEditar, onNovoProduto, atualizarProdutos }) {
  const [termoBusca, setTermoBusca] = useState('');

  const excluirProduto = async (id) => {
    if (!window.confirm('Deseja excluir este produto?')) return;
    await fetch(`http://localhost:8000/produtos/${id}`, { method: 'DELETE' });
    atualizarProdutos();
  };

  const calcularValorVenda = (p) => {
    const custoUnitario = p.valor_total / p.quantidade_total;
    const imposto = custoUnitario * (p.aliquota_imposto / 100);
    const gastos = custoUnitario * (p.gastos_fixos / 100);
    const lucro = custoUnitario * (p.margem_lucro / 100);
    return (custoUnitario + imposto + gastos + lucro).toFixed(2);
  };

  const produtosFiltrados = produtos.filter((p) =>
    p.nome_produto.toLowerCase().includes(termoBusca.toLowerCase()) ||
    p.codigo_barras.toLowerCase().includes(termoBusca.toLowerCase())
  );

  return (
    <div style={{
      maxWidth: '1100px',
      margin: '2rem auto',
      padding: '1.5rem',
      backgroundColor: '#f9f9f9',
      borderRadius: '12px',
      boxShadow: '0 0 10px rgba(0,0,0,0.1)'
    }}>
      <h2 style={{
        textAlign: 'center',
        marginBottom: '1.5rem',
        fontSize: '1.8rem'
      }}>
        📦 Lista de Produtos
      </h2>

      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem',
        marginBottom: '1rem'
      }}>
        <div style={{ position: 'relative', flex: '1 1 250px', maxWidth: '300px' }}>
          <span
            style={{
              position: 'absolute',
              top: '50%',
              left: '10px',
              transform: 'translateY(-50%)',
              color: '#888',
              pointerEvents: 'none',
              fontSize: '18px'
            }}
          >
            🔍
          </span>
          <input
            type="text"
            placeholder="Buscar por nome ou código de barras..."
            value={termoBusca}
            onChange={(e) => setTermoBusca(e.target.value)}
            style={{
              padding: '8px 8px 8px 32px',
              borderRadius: '15px',
              border: '1px solid #ccc',
              width: '100%',
              fontSize: '14px',
              outline: 'none'
            }}
          />
        </div>

        <button
          onClick={onNovoProduto}
          style={{
            padding: '8px 16px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '15px',
            cursor: 'pointer',
            fontWeight: 'bold',
            height: '40px',
            whiteSpace: 'nowrap'
          }}
        >
          + Cadastrar Produto
        </button>
      </div>

      <table style={{
        width: '100%',
        borderCollapse: 'collapse',
        backgroundColor: 'white',
        borderRadius: '10px',
        overflow: 'hidden'
      }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0', color: '#333' }}>
            <th style={th}>Código de Barras</th>
            <th style={th}>Nome</th>
            <th style={th}>Qtd</th>
            <th style={th}>Valor Total</th>
            <th style={th}>Unitário</th>
            <th style={th}>Imposto (%)</th>
            <th style={th}>Fixos (%)</th>
            <th style={th}>Lucro (%)</th>
            <th style={th}>Venda</th>
            <th style={th}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {produtosFiltrados.map((p, index) => (
            <tr
              key={p.id}
              style={{
                backgroundColor: index % 2 === 0 ? '#fff' : '#fafafa',
                borderBottom: '1px solid #ddd'
              }}
            >
              <td style={td}>{p.codigo_barras}</td>
              <td style={td}>{p.nome_produto}</td>
              <td style={td}>{p.quantidade_total}</td>
              <td style={td}>R$ {p.valor_total.toFixed(2)}</td>
              <td style={td}>R$ {(p.valor_total / p.quantidade_total).toFixed(2)}</td>
              <td style={td}>{p.aliquota_imposto}%</td>
              <td style={td}>{p.gastos_fixos}%</td>
              <td style={td}>{p.margem_lucro}%</td>
              <td style={td}>R$ {calcularValorVenda(p)}</td>
              <td style={{ ...td, textAlign: 'center' }}>
                <button
                  onClick={() => onEditar(p)}
                  style={editBtn}
                >
                  ✏️
                </button>
                <button
                  onClick={() => excluirProduto(p.id)}
                  style={deleteBtn}
                >
                  🗑️
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const th = {
  padding: '10px',
  textAlign: 'left',
  fontWeight: 'bold',
  borderBottom: '2px solid #ddd'
};

const td = {
  padding: '10px',
  fontSize: '14px',
  verticalAlign: 'middle'
};

const editBtn = {
  padding: '6px 10px',
  marginRight: '6px',
  backgroundColor: '#2196F3',
  color: 'white',
  border: 'none',
  borderRadius: '15px',
  cursor: 'pointer'
};

const deleteBtn = {
  padding: '6px 10px',
  backgroundColor: '#f44336',
  color: 'white',
  border: 'none',
  borderRadius: '15px',
  cursor: 'pointer'
};

export default ListaProdutos;
