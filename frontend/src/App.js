import React, { useState, useEffect } from 'react';
import ListaProdutos from './ListaProdutos';

function App() {
  const [produtos, setProdutos] = useState([]);
  const [modoEdicao, setModoEdicao] = useState(false);
  const [salvando, setSalvando] = useState(false);
  const [mensagem, setMensagem] = useState('');
  const [termoBusca, setTermoBusca] = useState('');
  const [form, setForm] = useState({
    id: null,
    nome_produto: '',
    codigo_barras: '',
    quantidade_total: '',
    valor_total: '',
    aliquota_imposto: '',
    margem_lucro: '',
    gastos_fixos: '',
  });

  useEffect(() => {
    fetchProdutos();
  }, []);

  const fetchProdutos = async () => {
    try {
      const res = await fetch('http://localhost:8000/produtos/');
      const data = await res.json();
      setProdutos(data);
    } catch (error) {
      console.error('Erro ao buscar produtos:', error);
    }
  };

  const handleEditar = (produto) => {
    setModoEdicao(true);
    setForm(produto);
  };

  const handleNovoProduto = () => {
    setModoEdicao(true);
    setForm({
      id: null,
      nome_produto: '',
      codigo_barras: '',
      quantidade_total: '',
      valor_total: '',
      aliquota_imposto: '',
      margem_lucro: '',
      gastos_fixos: '',
    });
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    setSalvando(true);

    const produtoExistente = produtos.find(
      (p) =>
        p.nome_produto.toLowerCase() === form.nome_produto.toLowerCase() ||
        p.codigo_barras === form.codigo_barras
    );

    if (!form.id && produtoExistente) {
      setMensagem('Produto já cadastrado com esse nome ou código de barras!');
      setSalvando(false);
      setTimeout(() => setMensagem(''), 3000);
      return;
    }

    const metodo = modoEdicao && form.id ? 'PUT' : 'POST';
    const url =
      metodo === 'PUT'
        ? `http://localhost:8000/produtos/${form.id}`
        : 'http://localhost:8000/produtos/';

    try {
      const res = await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        await fetchProdutos();
        setMensagem(`Produto ${form.id ? 'atualizado' : 'cadastrado'} com sucesso!`);
        setTimeout(() => setMensagem(''), 3000);
        setModoEdicao(false);
        setForm({
          id: null,
          nome_produto: '',
          codigo_barras: '',
          quantidade_total: '',
          valor_total: '',
          aliquota_imposto: '',
          margem_lucro: '',
          gastos_fixos: '',
        });
      } else {
        setMensagem('Erro ao salvar produto.');
      }
    } catch (err) {
      setMensagem('Erro de rede.');
    } finally {
      setSalvando(false);
    }
  };

  const handleExcluir = async (id) => {
    const confirmar = window.confirm('Tem certeza que deseja excluir este produto?');
    if (!confirmar) return;

    try {
      const res = await fetch(`http://localhost:8000/produtos/${id}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        await fetchProdutos();
        setMensagem('Produto excluído com sucesso!');
        setTimeout(() => setMensagem(''), 3000);
      } else {
        setMensagem('Erro ao excluir produto.');
      }
    } catch (err) {
      setMensagem('Erro de rede.');
    }
  };

  return (
    <div style={{ padding: '1rem', fontFamily: 'Arial, sans-serif' }}>
      {mensagem && (
        <div style={{
          backgroundColor: '#d4edda',
          color: '#155724',
          padding: '10px',
          borderRadius: '8px',
          marginBottom: '1rem',
          textAlign: 'center'
        }}>
          {mensagem}
        </div>
      )}

      {!modoEdicao && (
        <ListaProdutos
          produtos={produtos}
          onEditar={handleEditar}
          onNovoProduto={handleNovoProduto}
          onExcluir={handleExcluir}
          termoBusca={termoBusca}
          setTermoBusca={setTermoBusca}
        />
      )}

      {modoEdicao && (
        <div
          style={{
            maxWidth: '600px',
            margin: '2rem auto',
            padding: '1.5rem',
            backgroundColor: '#f9f9f9',
            borderRadius: '12px',
            boxShadow: '0 0 10px rgba(0,0,0,0.1)'
          }}
        >
          <h2 style={{ textAlign: 'center', marginBottom: '1rem' }}>
            {form.id ? 'Editar Produto' : 'Cadastrar Produto'}
          </h2>

          {[
            { label: 'Nome do Produto', name: 'nome_produto' },
            { label: 'Código de Barras', name: 'codigo_barras' },
            { label: 'Quantidade Total', name: 'quantidade_total', type: 'number' },
            { label: 'Valor Total (R$)', name: 'valor_total', type: 'number' },
            { label: 'Alíquota de Imposto (%)', name: 'aliquota_imposto', type: 'number' },
            { label: 'Gastos Fixos (%)', name: 'gastos_fixos', type: 'number' },
            { label: 'Margem de Lucro (%)', name: 'margem_lucro', type: 'number' }
          ].map(({ label, name, type = 'text' }) => (
            <div key={name} style={{ marginBottom: '12px' }}>
              <label style={{ display: 'block', marginBottom: '4px', fontWeight: 'bold' }}>
                {label}
              </label>
              <input
                type={type}
                name={name}
                value={form[name]}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: '8px',
                  borderRadius: '8px',
                  border: '1px solid #ccc',
                  fontSize: '14px'
                }}
              />
            </div>
          ))}

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
            <button
              onClick={handleSubmit}
              disabled={salvando}
              style={{
                padding: '10px 20px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              {salvando ? 'Salvando...' : form.id ? 'Atualizar' : 'Cadastrar'}
            </button>
            <button
              onClick={() => setModoEdicao(false)}
              style={{
                padding: '10px 20px',
                backgroundColor: '#6b7280',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              Cancelar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
