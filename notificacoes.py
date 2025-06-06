from twilio.rest import Client
import requests
import os

# Configurações Twilio
ACCOUNT_SID = 'AC10716c6484795ad69ae58ef2e0959fb1'
AUTH_TOKEN = 'b30724424e25d0c00ab94262d191cbe0'
FROM_WHATSAPP = 'whatsapp:+14155238886' # Número do Sandbox Twilio
TO_WHATSAPP = 'whatsapp:+5511993031851' # Seu número (com código país)
#TO_WHATSAPP_LIST = [
 #   'whatsapp:+558499841613',
 #   'whatsapp:+558481727000'
#]


def enviar_whatsapp(titulo, url_documento):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Baixar arquivo para enviar via WhatsApp
    nome_arquivo = url_documento.split('/')[-1].split('?')[0]
    resposta = requests.get(url_documento)

    if resposta.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            f.write(resposta.content)
    else:
        print(f"Erro ao baixar o arquivo: {url_documento}")
        return

    # Subir o arquivo para um local acessível (necessário para o Twilio)
    # O Twilio exige URL pública para arquivos. Para simplificar, você pode subir para algum storage (AWS S3, Google Drive público, Dropbox público)
    # Como exemplo inicial, enviaremos apenas a mensagem com o link (sem anexo direto):

    mensagem = f"*Novo documento MME disponível:*\n\n{titulo}\n\nLink: {url_documento}"

    try:
        message = client.messages.create(
            from_=FROM_WHATSAPP,
            body=mensagem,
            to=TO_WHATSAPP
        )
        print(f"WhatsApp enviado com sucesso! SID: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar WhatsApp: {e}")
    finally:
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)  # Limpa o arquivo local



import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

SENDGRID_API_KEY = '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'
EMAIL_REMETENTE = 'fortescuenotifications@gmail.com'
EMAIL_DESTINATARIO = 'lierbetmedeiros@gmail.com'
EMAILS_DESTINATARIOS = [
    'lierbetmedeiros@gmail.com',
    'camila.neves@fortescue.com',
    'rafael.maia@fortescue.com'
]

def enviar_email(titulo, url_documento):
    nome_arquivo = url_documento.rstrip('/').split('/')[-1].split('?')[0]

    if not nome_arquivo:
        nome_arquivo = "documento_baixado.pdf"

    resposta = requests.get(url_documento)
    if resposta.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            f.write(resposta.content)
    else:
        print(f"Erro ao baixar arquivo: {url_documento}")
        return

    with open(nome_arquivo, 'rb') as f:
        arquivo_dados = f.read()
        arquivo_b64 = base64.b64encode(arquivo_dados).decode()

    message = Mail(
        from_email=EMAIL_REMETENTE,
        to_emails=EMAIL_DESTINATARIO,
        subject=f"[MME] Novo documento: {titulo}",
        plain_text_content=f"Novo documento disponível:\n\n{titulo}\n\nLink direto: {url_documento}"
    )

    attachment = Attachment(
        FileContent(arquivo_b64),
        FileName(nome_arquivo),
        FileType('application/octet-stream'),
        Disposition('attachment')
    )
    message.attachment = attachment

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email enviado! Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar email via SendGrid API: {e}")
    finally:
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)


import asyncio
from telegram import Bot

TELEGRAM_TOKEN = "8026252273:AAFIOA18VOQrX_PhJrDJ2zg6R5yTPvOgN4Q"
TELEGRAM_CHAT_ID = "-4980332586"

async def enviar_telegram(titulo, url_documento):
    bot = Bot(token=TELEGRAM_TOKEN)
    mensagem = f"📢 *Novo documento publicado no MME!*\n\n*{titulo}*\n[Clique para acessar o documento]({url_documento})"

    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=mensagem,
            parse_mode='Markdown'
        )
        print(f"Telegram enviado com sucesso: {titulo}")
    except Exception as e:
        print(f"Erro ao enviar mensagem no Telegram: {e}")

