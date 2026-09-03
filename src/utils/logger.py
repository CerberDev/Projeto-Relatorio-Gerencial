import logging
from pathlib import Path

# Configurar o local exato onde os arquivos de registro serão salvos
ROOT_DIR     = Path(__file__).resolve().parents[2]
LOG_EXECUCAO = ROOT_DIR / 'logs' / 'execucao.log'
LOG_ERROS    = ROOT_DIR / 'logs' / 'erro.log'

# Função para preparar e entregar o sistema de registros
def get_logger(name: str = 'vendas') -> logging.Logger:
    logger = logging.getLogger(name)

    # Se o sistema de registros já estiver pronto, apenas devolve ele (evita repetições)
    if logger.handlers:
        return logger

    # Define que o sistema deve prestar atenção em todos os tipos de mensagens
    logger.setLevel(logging.DEBUG)

    # Impede que a mesma mensagem seja repassada e mostrada duas vezes
    logger.propagate = False

    # Define qual será a aparência do texto salvo (data, tipo, nome e a mensagem em si)
    formatador = logging.Formatter(
        '%(asctime)s | [%(levelname)s] | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Cria a pasta 'logs' no computador, caso ela ainda não exista
    LOG_EXECUCAO.parent.mkdir(parents=True, exist_ok=True)
    LOG_ERROS.parent.mkdir(parents=True, exist_ok=True)

    # --- Configurar para onde as mensagens serão enviadas ---

    # 1. Mostrar as mensagens normais na tela preta (terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatador)
    logger.addHandler(console_handler) # Conecta essa configuração ao nosso registro principal

    # 2. Salvar as mensagens normais no arquivo "execucao.log"
    file_execucao = logging.FileHandler(LOG_EXECUCAO,encoding='utf-8')
    file_execucao.setLevel(logging.INFO)
    file_execucao.setFormatter(formatador)
    logger.addHandler(file_execucao)

    # 3. Salvar apenas os problemas graves no arquivo "erro.log"
    file_erros = logging.FileHandler(LOG_ERROS,encoding='utf-8')
    file_erros.setLevel(logging.ERROR)
    file_erros.setFormatter(formatador)
    logger.addHandler(file_erros)

    return logger