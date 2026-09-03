import smtplib
from email.message import EmailMessage
import logging
from src.utils.env_loader import get_credenciais_email
import sys

#Configuração do logger para poder aparecer também como um print
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# O if é para garantir que não vai duplicar as mensagens se o módulo for carregado
if not logger.handlers:
    # cria o log para aparecer igual ao print
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

# Formatação da mensagem
formatador = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s', datefmt='%H:%M:%S')
console_handler.setFormatter(formatador)
# mostra as mensagens na tela
logger.addHandler(console_handler)


# Estas variáveis ficam no escopo do arquivo
config = get_credenciais_email()

def _conectar():
    """Função interna, privada do módulo. O Underline avisa para não usarem fora do módulo"""
    try:
        logger.info("Abrindo conexão com o servidor do e-mail...")
        server = smtplib.SMTP(config['host'], config['port'])
        server.starttls()
        server.login(config['user'], config['password'])
        logger.info("Conexão realizada com sucesso!")
        return server
    except Exception as e:
        logger.error(f"Falha na conexão SMTP: {e}")
        raise

def _montar_mensagem(destinatarios, assunto, corpo):
    """Função interna privada para estruturar o payload"""
    msg = EmailMessage()
    msg['From'] = config.get('user')
    msg['To'] = destinatarios if isinstance(destinatarios, str) else ', '.join(destinatarios)
    msg['Subject'] = assunto
    msg.set_content(corpo)
    logger.info("Mensagem montada com sucesso!")
    return msg

def enviar_mensagem(destinatarios: list, assunto: str, corpo: str):
    """Função publica exposta para todo o projeto"""
    server = None
    try:
        logger.info("Enviando e-mail...")
        msg = _montar_mensagem(destinatarios, assunto, corpo)
        server = _conectar()
        server.send_message(msg)
        logger.info(f"E-mail enviado para os destinatarios - {destinatarios} - com sucesso!")
    except Exception as e:
        logger.error(f"Erro no envio do e-mail - {e}")
    finally:
        if server:
            server.quit()
            logger.info("Conexão SMPT encerrada")


