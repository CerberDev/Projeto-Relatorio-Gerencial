import pandas as pd
from src.utils.logger import get_logger
from src.utils.email_service import enviar_mensagem
from src.utils.extracao import carregar_dados
from src.utils.tratamento import tratar_dados
from src.utils.integracao import integrar_dados
from src.utils.regras_negocio import calcular_indicadores

logger = get_logger('main')

def formatar_corpo_email(nome_gestor, indicadores):
    """Cria a string formatada do e-mail em texto puro/estruturado com base nos indicadores calculados."""
    st = indicadores['contagem_status']
    
    if indicadores['lista_vencidos']:
        lista_colaboradores = "\n".join([
            f"  - {item['colaborador_nome']} | Curso: {item['treinamento']} | Vencimento: {item['data_limite'].strftime('%d/%m/%Y')}" 
            for item in indicadores['lista_vencidos']
        ])
    else:
        lista_colaboradores = "  Nenhum treinamento vencido."
    
    corpo = f"""Olá, {nome_gestor}. Segue o relatório gerencial consolidado da sua área:

=== Bloco 1: Projetos sob sua responsabilidade ===
- Total de Projetos: {indicadores['total_projetos']}
- Em andamento: {st.get('Em andamento', 0)}
- Atrasados: {st.get('Atrasado', 0)}
- Concluídos no prazo: {st.get('Concluído dentro do prazo', 0)}
- Concluídos com atraso: {st.get('Concluído com atraso', 0)}
- % Médio de Execução (em andamento/atrasados): {indicadores['perc_medio_concluido']:.2f}%
- Tempo Médio de Duração (projetos concluídos): {indicadores['tempo_medio_duracao']:.1f} dias
- Valor Total Orçado: R$ {indicadores['valor_total_orcado']:,.2f}

=== Bloco 2: Treinamentos da sua Área ===
- Treinamentos Pendentes (Total não concluídos): {indicadores['qtd_pendentes']}
- Treinamentos Vencidos: {indicadores['qtd_vencidos']}
- % de Conformidade (Concluídos / Total da área): {indicadores['perc_conformidade']:.2f}%

Colaboradores com treinamentos vencidos (Cobrança imediata requerida):
{lista_colaboradores}

Atenciosamente,
Automação Gerencial
"""
    return corpo

def main():
    logger.info("Iniciando Automação RPA...")
    try:
        df_gestores, df_status, df_rh = carregar_dados()
        df_gestores, df_status, df_rh = tratar_dados(df_gestores, df_status, df_rh)
        df_projetos = integrar_dados(df_gestores, df_status)
        
        gestores_projetos_unicos = df_projetos[['gestor_id', 'gestor_nome', 'email_gestor', 'area']].drop_duplicates()
        emails_enviados = 0
        
        # Lista dos e-mails reais que receberão os relatórios (rodízio)
        lista_emails_reais = [
            'elzaesimoes@gmail.com', 
            'eguilherme709@gmail.com', 
            'alessandrofranca7@gmail.com'
        ]
        
        # Usamos enumerate para ter um contador 'i' e fazer a distribuição
        for i, (idx, row) in enumerate(gestores_projetos_unicos.iterrows()):
            gestor_id = row['gestor_id']
            nome_gestor = row['gestor_nome']
            email_ficticio = row['email_gestor']
            area = row['area']
            
            indicadores = calcular_indicadores(df_projetos, df_rh, gestor_id)
            corpo_email = formatar_corpo_email(nome_gestor, indicadores)
            
            # Escolhe o e-mail da vez na lista com base na posição
            email_destino = lista_emails_reais[i % len(lista_emails_reais)]
            
            # Colocando no assunto de quem era originalmente para você conseguir validar
            assunto = f"[Redirecionado de {email_ficticio}] Relatório Gerencial - Área: {area}"
            
            enviar_mensagem([email_destino], assunto, corpo_email)
            emails_enviados += 1
            
        # Avaliação do Desafio: Envio do relatório simulado ao e-mail do professor
        if not gestores_projetos_unicos.empty:
            logger.info("Enviando resultado de simulação para o professor responsável...")
            primeiro_gestor = gestores_projetos_unicos.iloc[0]
            inds_prof = calcular_indicadores(df_projetos, df_rh, primeiro_gestor['gestor_id'])
            corpo_prof = formatar_corpo_email(primeiro_gestor['gestor_nome'], inds_prof)
            
            # Envia o teste do professor em cópia para a sua lista também para garantir que você veja
            destinatarios_prof = ['prof.leandrolessa@gmail.com'] + lista_emails_reais
            
            enviar_mensagem(
                destinatarios_prof, 
                f"Desafio Final RPA - Relatório Simulado ({primeiro_gestor['area']})", 
                corpo_prof
            )
            
        logger.info(f"Automação finalizada! {emails_enviados} relatórios de gestores enviados.")
        
    except Exception as e:
        logger.error(f"Erro fatal na execução do processo: {e}")


if __name__ == '__main__':
    main()