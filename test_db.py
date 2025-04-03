from sqlalchemy import create_engine, text

# URL de conexão com o banco de dados
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:teste@localhost:8280/calculadora_custos"

# Criação do motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Teste de conexão e leitura de dados
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM produtos LIMIT 5"))
        for row in result:
            print(row)
    print("Conexão bem-sucedida!")
except Exception as e:
    print(f"Erro de conexão: {e}")
