from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# URL de conexão com o banco de dados
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Criar conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criar sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base dos modelos
Base = declarative_base()

# Criar tabelas no banco de dados
def criar_tabelas():
    Base.metadata.create_all(bind=engine)

criar_tabelas()
