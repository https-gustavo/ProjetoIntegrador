from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados na Railway
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:FGuJhYAVyAtiugBcayNwSqejXyjbjMUv@switchback.proxy.rlwy.net:59685/railway"

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
