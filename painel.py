from flask import Flask, render_template_string
import os

app = Flask(__name__)

LOG_PATH = "/opt/monitoramento_mme/cron.log"

HTML_TEMPLATE = """
<!doctype html>
<html lang="pt-br">
  <head>
    <meta charset="utf-8">
    <title>Monitoramento MME - Logs</title>
    <style>
      body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
      h1 { color: #0f0; }
      pre { white-space: pre-wrap; word-wrap: break-word; background: #222; padding: 10px; border-radius: 8px; }
    </style>
  </head>
  <body>
    <h1>🛰️ Logs do Monitoramento MME</h1>
    <pre>{{ log_content }}</pre>
  </body>
</html>
"""

@app.route("/")
def exibir_logs():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            log_content = f.read()[-10000:]  # últimos 10.000 caracteres
    else:
        log_content = "Arquivo de log não encontrado."
    return render_template_string(HTML_TEMPLATE, log_content=log_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
