from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# String de conexão com o banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:teste@localhost:8280/calculadora_custos"

# Criação do engine para conexão com o banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base das tabelas
Base = declarative_base()
