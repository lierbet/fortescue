import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin
from notificacoes import enviar_whatsapp, enviar_email
import asyncio
from notificacoes import enviar_telegram

URL_BASE = "https://www.gov.br"
URL_PAGINA = "https://www.gov.br/mme/pt-br/assuntos/secretarias/sntep/publicacoes/plano-de-outorgas-de-transmissao-de-energia-eletrica-potee/documentos/2025"

DB = "historico.db"

def criar_banco():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            url TEXT PRIMARY KEY,
            titulo TEXT,
            data_adicionado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def buscar_novos_documentos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    response = requests.get(URL_PAGINA, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a', href=True)

    novos_documentos = []

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    for link in links:
        href = link['href'].lower()
        if any(ext in href for ext in ['.pdf', '.xls', '.xlsx']):
            titulo = link.get_text(strip=True)
            url_completa = urljoin(URL_BASE, href)

            cursor.execute("SELECT 1 FROM documentos WHERE url = ?", (url_completa,))
            if cursor.fetchone() is None:
                novos_documentos.append({"titulo": titulo, "url": url_completa})
                cursor.execute("INSERT INTO documentos (url, titulo) VALUES (?, ?)", (url_completa, titulo))

    conn.commit()
    conn.close()
    return novos_documentos

# Teste isolado
if __name__ == "__main__":
    criar_banco()
    novos = buscar_novos_documentos()
    if novos:
        print(f"Novos documentos encontrados: {len(novos)}")
        for doc in novos:
            print(f"- {doc['titulo']} -> {doc['url']}")
            enviar_whatsapp(doc["titulo"], doc["url"])
            enviar_email(doc["titulo"], doc["url"])
            asyncio.run(enviar_telegram(doc["titulo"], doc["url"]))
    else:
        print("Nenhum novo documento encontrado.")

