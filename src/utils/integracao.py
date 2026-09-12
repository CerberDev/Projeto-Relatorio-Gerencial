import pandas as pd
from src.utils.logger import get_logger

logger = get_logger('integracao')

def integrar_dados(df_gestores, df_status):
    """Realiza o join (inner) das tabelas gestores e status utilizando a chave 'codigo_projeto'."""
    logger.info("Iniciando integração dos dados...")
    try:
        df_projetos = pd.merge(df_gestores, df_status, on='codigo_projeto', how='inner')
        logger.info("Integração concluída com sucesso.")
        return df_projetos
    except Exception as e:
        logger.error(f"Erro na integração dos dados: {e}")
        raise