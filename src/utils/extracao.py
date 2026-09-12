import pandas as pd
from src.utils.path_manager import RAW_DIR
from src.utils.logger import get_logger

logger = get_logger('extracao')

def carregar_dados():
    """Lê os arquivos CSV da pasta raw e retorna os DataFrames."""
    logger.info("Iniciando extração dos dados brutos...")
    try:
        df_gestores = pd.read_csv(RAW_DIR / 'gestores_projetos.csv')
        df_status = pd.read_csv(RAW_DIR / 'status_projetos.csv')
        df_rh = pd.read_csv(RAW_DIR / 'rh_treinamentos.csv')
        
        logger.info("Extração concluída com sucesso.")
        return df_gestores, df_status, df_rh
    except Exception as e:
        logger.error(f"Erro na extração dos dados: {e}")
        raise