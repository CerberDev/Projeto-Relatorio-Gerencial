import pandas as pd
from src.utils.logger import get_logger

logger = get_logger('regras_negocio')

def classificar_status(row):
    """Define a situação do projeto baseada na comparação entre hoje, fim previsto e conclusão."""
    hoje = pd.Timestamp.now()
    prev_fim = row['data_prevista_fim']
    conclusao = row['data_conclusao']
    
    if pd.isna(conclusao):
        if pd.notna(prev_fim) and hoje > prev_fim:
            return 'Atrasado'
        return 'Em andamento'
    else:
        if pd.notna(prev_fim) and conclusao > prev_fim:
            return 'Concluído com atraso'
        return 'Concluído dentro do prazo'

def calcular_indicadores(df_projetos, df_rh, gestor_id):
    """Calcula os KPIs exigidos para os Blocos 1 (Projetos) e 2 (RH) por gestor."""
    # Filtrar projetos do gestor correspondente
    df_proj_filtrado = df_projetos[df_projetos['gestor_id'] == gestor_id].copy()
    
    if not df_proj_filtrado.empty:
        df_proj_filtrado['situacao'] = df_proj_filtrado.apply(classificar_status, axis=1)
    else:
        df_proj_filtrado['situacao'] = pd.Series(dtype='object')
    
    # === Bloco 1: Projetos ===
    total_projetos = len(df_proj_filtrado)
    contagem_status = df_proj_filtrado['situacao'].value_counts().to_dict()
    
    projetos_nao_concluidos = df_proj_filtrado[df_proj_filtrado['situacao'].isin(['Em andamento', 'Atrasado'])]
    perc_medio_concluido = projetos_nao_concluidos['percentual_concluido'].mean() if not projetos_nao_concluidos.empty else 0
    
    projetos_concluidos = df_proj_filtrado[df_proj_filtrado['situacao'].isin(['Concluído dentro do prazo', 'Concluído com atraso'])]
    if not projetos_concluidos.empty:
        duracao = (projetos_concluidos['data_conclusao'] - projetos_concluidos['data_inicio']).dt.days
        tempo_medio_duracao = duracao.mean()
    else:
        tempo_medio_duracao = 0
        
    valor_total_orcado = df_proj_filtrado['valor_orcado'].sum()

    # === Bloco 2: RH ===
    # O gestor na base de RH atende pela coluna gestor_id_area
    df_rh_filtrado = df_rh[df_rh['gestor_id_area'] == gestor_id].copy()
    hoje = pd.Timestamp.now()
    
    total_treinamentos = len(df_rh_filtrado)
    df_concluidos = df_rh_filtrado[df_rh_filtrado['status_treinamento'] == 'Concluído']
    df_pendentes = df_rh_filtrado[df_rh_filtrado['status_treinamento'] != 'Concluído']
    
    qtd_pendentes = len(df_pendentes)
    # Vencido = não concluído E com a data limite menor que hoje
    df_vencidos = df_pendentes[df_pendentes['data_limite'] < hoje]
    qtd_vencidos = len(df_vencidos)
    
    qtd_concluidos = len(df_concluidos)
    perc_conformidade = (qtd_concluidos / total_treinamentos * 100) if total_treinamentos > 0 else 0
    
    # Listagem nominal de colaboradores com treino vencido
    lista_vencidos = df_vencidos[['colaborador_nome', 'treinamento', 'data_limite']].to_dict('records')

    return {
        'total_projetos': total_projetos,
        'contagem_status': contagem_status,
        'perc_medio_concluido': perc_medio_concluido,
        'tempo_medio_duracao': tempo_medio_duracao,
        'valor_total_orcado': valor_total_orcado,
        'qtd_pendentes': qtd_pendentes,
        'qtd_vencidos': qtd_vencidos,
        'perc_conformidade': perc_conformidade,
        'lista_vencidos': lista_vencidos
    }