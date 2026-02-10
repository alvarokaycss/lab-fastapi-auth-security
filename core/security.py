from passlib.context import CryptContext

# Cria uma instância de CryptContext para gerenciar o hash de senhas
CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Codifica uma senha utilizando bcrypt e retorna o hash
    """
    return CRIPTO.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha corresponde a uma hash utilizando bcrypt e retorna True se corresponder, False caso contrário
    """
    return CRIPTO.verify(password, hashed_password)
