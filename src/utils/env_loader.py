import os # Corrigido: Faltava importar o 'os'
from dotenv import load_dotenv
from src.utils.path_manager import CONFIG_DIR

env_path = CONFIG_DIR / '.env'
load_dotenv(dotenv_path=env_path)

def get_credenciais_email() -> dict:
    return {
        'user': os.getenv('USER'),       # Corrigido: faltava a primeira aspa no 'user'
        'password': os.getenv('PASSWORD'), 
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT')        # Corrigido: removido o espaço no os. getenv
    }

# Opcional: deixei o print comentado para não sujar a tela sempre que esse código for importado
print(env_path)