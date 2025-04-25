from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criptografar a senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar a senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
