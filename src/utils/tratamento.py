import pandas as pd
from src.utils.logger import get_logger

logger = get_logger('tratamento')

def padronizar_texto(series, formato='title'):
    """Remove espaços em branco nas pontas e padroniza a caixa do texto."""
    serie_limpa = series.astype(str).str.strip()
    if formato == 'title':
        return serie_limpa.str.title()
    elif formato == 'lower':
        return serie_limpa.str.lower()
    return serie_limpa

def tratar_dados(df_gestores, df_status, df_rh):
    """Executa a limpeza, formatação e padronização das bases."""
    logger.info("Iniciando tratamento dos dados...")
    try:
        # Remoção de duplicatas explícita
        df_gestores = df_gestores.drop_duplicates().copy()
        df_status = df_status.drop_duplicates().copy()
        df_rh = df_rh.drop_duplicates().copy()

        # Padronização de chaves primárias e estrangeiras
        df_gestores['codigo_projeto'] = df_gestores['codigo_projeto'].astype(str).str.strip()
        df_status['codigo_projeto'] = df_status['codigo_projeto'].astype(str).str.strip()
        df_gestores['gestor_id'] = df_gestores['gestor_id'].astype(str).str.strip()
        df_rh['gestor_id_area'] = df_rh['gestor_id_area'].astype(str).str.strip()

        # Padronização de áreas, nomes e e-mails para evitar agrupamentos incorretos
        df_gestores['area'] = padronizar_texto(df_gestores['area'], 'title')
        df_rh['area'] = padronizar_texto(df_rh['area'], 'title')
        
        df_gestores['gestor_nome'] = padronizar_texto(df_gestores['gestor_nome'], 'title')
        df_rh['colaborador_nome'] = padronizar_texto(df_rh['colaborador_nome'], 'title')
        
        df_gestores['email_gestor'] = padronizar_texto(df_gestores['email_gestor'], 'lower')
        df_rh['email_gestor_area'] = padronizar_texto(df_rh['email_gestor_area'], 'lower')

        # O que for nulo em status_treinamento consideramos "Pendente"
        df_rh['status_treinamento'] = df_rh['status_treinamento'].fillna('Pendente').str.strip().str.title()

        # Conversão de Datas considerando formatos mistos nas bases 
        colunas_status = ['data_inicio', 'data_prevista_fim', 'data_conclusao']
        for col in colunas_status:
            # dayfirst=True assegura que formatos como 17-07-2026 sejam lidos como (dia-mes-ano)
            df_status[col] = pd.to_datetime(df_status[col], format='mixed', dayfirst=True, errors='coerce')

        df_rh['data_limite'] = pd.to_datetime(df_rh['data_limite'], format='mixed', dayfirst=True, errors='coerce')

        logger.info("Tratamento concluído com sucesso.")
        return df_gestores, df_status, df_rh
    except Exception as e:
        logger.error(f"Erro no tratamento dos dados: {e}")
        raise