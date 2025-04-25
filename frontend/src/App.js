import React, { useState, useEffect } from 'react';
import ListaProdutos from './ListaProdutos';

const API_URL = 'https://postgres-production-c3cb.up.railway.app';

// --- Estilos compartilhados ---
const styles = {
  body: {
    height: '100vh',
    background: '#f2f2f2',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'Arial, sans-serif'
  },
  container: {
    background: 'white',
    padding: 30,
    borderRadius: 12,
    boxShadow: '0 0 15px rgba(0,0,0,0.1)',
    maxWidth: 400,
    width: '100%',
    textAlign: 'center'
  },
  label: {
    display: 'block',
    textAlign: 'left',
    marginBottom: 4,
    fontWeight: 'bold'
  },
  input: {
    width: '100%',
    padding: 10,
    marginBottom: 16,
    border: '1px solid #ccc',
    borderRadius: 8,
    boxSizing: 'border-box'
  },
  button: {
    padding: 12,
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: 8,
    fontSize: 16,
    cursor: 'pointer'
  },
  linkText: {
    marginTop: 10,
    fontSize: 14,
    color: '#007bff',
    textDecoration: 'underline',
    cursor: 'pointer'
  },
  mensagem: {
    marginTop: 16,
    fontWeight: 'bold',
    color: '#d9534f'
  },
  popup: {
    position: 'fixed',
    top: 20,
    left: '50%',
    transform: 'translateX(-50%)',
    background: '#333',
    color: '#fff',
    padding: '10px 20px',
    borderRadius: 8
  },
  form: {
    maxWidth: 600,
    margin: '2rem auto',
    padding: '1.5rem',
    background: '#f9f9f9',
    borderRadius: 12,
    boxShadow: '0 0 10px rgba(0,0,0,0.1)'
  },
  btnCancel: {
    padding: '10px 20px',
    backgroundColor: 'red',
    color: '#fff',
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    fontWeight: 'bold',
    marginLeft: 10
  }
};

function TelaLogin({ onLogin }) {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [modoCadastro, setModoCadastro] = useState(false);

  const alternarFormulario = () => {
    setMensagem('');
    setModoCadastro(!modoCadastro);
  };

  const realizarLogin = async () => {
    if (!email || !senha) {
      setMensagem('Por favor, preencha todos os campos.');
      return;
    }
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });
      if (!res.ok) {
        const erro = await res.json();
        throw new Error(erro.detail || 'Erro ao fazer login');
      }
      const data = await res.json();
      localStorage.setItem('auth', JSON.stringify(data));
      setMensagem('Login bem-sucedido!');
      setTimeout(() => onLogin(data), 500);
    } catch (error) {
      setMensagem(error.message);
    }
  };

  const criarConta = async () => {
    if (!email || !senha) {
      setMensagem('Por favor, preencha todos os campos.');
      return;
    }
    try {
      const res = await fetch(`${API_URL}/usuarios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });
      if (!res.ok) {
        const erro = await res.json();
        throw new Error(erro.detail || 'Erro ao criar conta');
      }
      setMensagem('Conta criada com sucesso! Agora você pode fazer login.');
      setTimeout(() => setModoCadastro(false), 2000);
    } catch (error) {
      setMensagem(error.message);
    }
  };

  return (
    <div style={styles.body}>
      <div style={styles.container}>
        <h2>{modoCadastro ? 'Criar Conta' : 'Login'}</h2>

        <label style={styles.label}>Usuário:</label>
        <input
          type="email"
          value={email}
          placeholder="Digite seu Usuário"
          onChange={e => setEmail(e.target.value)}
          style={styles.input}
        />

        <label style={styles.label}>Senha:</label>
        <input
          type="password"
          value={senha}
          placeholder="Digite sua senha"
          onChange={e => setSenha(e.target.value)}
          style={styles.input}
        />

        <button
          onClick={modoCadastro ? criarConta : realizarLogin}
          style={styles.button}
        >
          {modoCadastro ? 'Cadastrar' : 'Entrar'}
        </button>

        <div onClick={alternarFormulario} style={styles.linkText}>
          {modoCadastro ? 'Voltar para o Login' : 'Criar Conta'}
        </div>

        {mensagem && <div style={styles.mensagem}>{mensagem}</div>}
      </div>
    </div>
  );
}

function App() {
  const [auth, setAuth] = useState(() => {
    const saved = localStorage.getItem('auth');
    return saved ? JSON.parse(saved) : null;
  });
  const [produtos, setProdutos] = useState([]);
  const [modoEdicao, setModoEdicao] = useState(false);
  const [popup, setPopup] = useState(null);
  const [form, setForm] = useState({
    id: null,
    nome_produto: '',
    codigo_barras: '',
    quantidade_total: '',
    valor_total: '',
    aliquota_imposto: '',
    margem_lucro: '',
    gastos_fixos: ''
  });

  const headersComAuth = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${auth.access_token}`
  });

  useEffect(() => {
    if (auth) atualizarProdutos();
  }, [auth]);

  const atualizarProdutos = async () => {
    try {
      const res = await fetch(`${API_URL}/produtos`, {
        headers: headersComAuth()
      });
      const data = await res.json();
      setProdutos(Array.isArray(data) ? data : []);
    } catch {
      setProdutos([]);
    }
  };

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });
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
      gastos_fixos: ''
    });
  };
  const handleEditar = p => {
    setModoEdicao(true);
    setForm(p);
  };

  const handleSubmit = async () => {
    const body = {
      nome_produto: form.nome_produto,
      quantidade_total: Number(form.quantidade_total),
      valor_total: Number(form.valor_total),
      aliquota_imposto: Number(form.aliquota_imposto),
      margem_lucro: Number(form.margem_lucro),
      gastos_fixos: Number(form.gastos_fixos),
      codigo_barras: form.codigo_barras
    };
    const metodo = form.id ? 'PUT' : 'POST';
    const url = form.id
      ? `${API_URL}/produtos/${form.id}`
      : `${API_URL}/produtos`;
    try {
      const res = await fetch(url, {
        method: metodo,
        headers: headersComAuth(),
        body: JSON.stringify(body)
      });
      if (!res.ok) throw new Error();
      await atualizarProdutos();
      setModoEdicao(false);
      setPopup(form.id ? 'Atualizado!' : 'Cadastrado!');
      setForm({
        id: null,
        nome_produto: '',
        codigo_barras: '',
        quantidade_total: '',
        valor_total: '',
        aliquota_imposto: '',
        margem_lucro: '',
        gastos_fixos: ''
      });
    } catch {
      setPopup('Erro ao salvar');
    }
    setTimeout(() => setPopup(null), 2500);
  };

  if (!auth) {
    return <TelaLogin onLogin={setAuth} />;
  }

  const logout = () => {
    localStorage.removeItem('auth');
    setAuth(null);
  };

  return (
    <div style={{ fontFamily: 'Arial', padding: '1rem' }}>
      <div style={{ textAlign: 'right', marginBottom: '1rem' }}>
        <button
          onClick={logout}
          style={{
            padding: '6px 12px',
            backgroundColor: '#f44336',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>

      {popup && <div style={styles.popup}>{popup}</div>}

      {!modoEdicao ? (
        <ListaProdutos
          produtos={produtos}
          onEditar={handleEditar}
          onNovoProduto={handleNovoProduto}
          atualizarProdutos={atualizarProdutos}
        />
      ) : (
        <div style={styles.form}>
          <h2 style={{ textAlign: 'center', marginBottom: 16 }}>
            {form.id ? 'Editar Produto' : 'Cadastrar Produto'}
          </h2>
          {[
            { label: 'Nome do Produto', name: 'nome_produto' },
            { label: 'Código de Barras', name: 'codigo_barras' },
            { label: 'Quantidade Total', name: 'quantidade_total', type: 'number' },
            { label: 'Valor Total', name: 'valor_total', type: 'number' },
            { label: 'Alíquota de Imposto (%)', name: 'aliquota_imposto', type: 'number' },
            { label: 'Margem de Lucro (%)', name: 'margem_lucro', type: 'number' },
            { label: 'Gastos Fixos', name: 'gastos_fixos', type: 'number' }
          ].map(({ label, name, type = 'text' }) => (
            <div key={name} style={{ marginBottom: 12 }}>
              <label
                style={{ display: 'block', marginBottom: 4, fontWeight: 'bold', textAlign: 'left' }}
              >
                {label}
              </label>
              <input
                type={type}
                name={name}
                value={form[name]}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: 8,
                  borderRadius: 8,
                  border: '1px solid #ccc'
                }}
              />
            </div>
          ))}
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: 16 }}>
            <button onClick={() => setModoEdicao(false)} style={styles.btnCancel}>
              Cancelar
            </button>
            <button onClick={handleSubmit} style={styles.button}>
              {form.id ? 'Atualizar' : 'Cadastrar'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
