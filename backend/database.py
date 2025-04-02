from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:teste@localhost:8280/calculadora_custos"

# Criação do motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criação da sessão para comunicação com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definição de modelos
Base = declarative_base()

# Criar Tabelas no Banco de Dados
Base.metadata.create_all(bind=engine)