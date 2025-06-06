import asyncio
from notificacoes import enviar_telegram

asyncio.run(enviar_telegram(
    "Documento de Teste",
    "https://www.gov.br/mme/pt-br/assuntos/secretarias/sntep/publicacoes/plano-de-outorgas-de-transmissao-de-energia-eletrica-potee/documentos/2025/06_potee_2024_4_emissao_fevereiro_2025.pdf"
))

