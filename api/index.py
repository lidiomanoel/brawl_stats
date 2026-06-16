from http.server import BaseHTTPRequestHandler
import urllib.parse
import json
import traceback
import sys
import os

# Adiciona a raiz do projeto ao path para importar brawl_api no ambiente do Vercel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa o cliente da API da raiz do projeto
from brawl_api import BrawlStarsClient

# Token da API
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmZjg2YWNjLTNkOWQtNGYwYi1iZjE1LTdhNDdlOTYzODRjMiIsImlhdCI6MTc4MTQ3OTQwNCwic3ViIjoiZGV2ZWxvcGVyLzJiMjhiZWMxLWE4ZjEtODVjMC0yM2M0LTRhZjY2MDVkMTU2OSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTcwLjIzOS4xMTEuMTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.yRPlUGMchkXE1ZOdNQyrnudaMKn5nHrPIUALPJBTVXMH0FJ4XGVhk8uwgWC_FYMnQVU4f82-A3m6aVUjTidm-g"
client = BrawlStarsClient(API_TOKEN)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Responde à rota de estatísticas
        if path.startswith("/api/stats"):
            query_params = urllib.parse.parse_qs(parsed_url.query)
            tag = query_params.get("tag", [""])[0]
            
            if not tag:
                self.send_json_response(400, {"error": "A tag do jogador é obrigatória."})
                return
                
            try:
                # Obtém os dados completos através do cliente
                stats = client.get_complete_stats(tag)
                self.send_json_response(200, stats)
            except Exception as e:
                traceback.print_exc()
                status = 500
                msg = str(e)
                if "404" in msg:
                    status = 404
                    msg = "Jogador não encontrado. Verifique a Tag digitada."
                elif "403" in msg:
                    status = 403
                    msg = "Erro de autenticação ou restrição de IP com a API do Brawl Stars."
                self.send_json_response(status, {"error": msg})
        else:
            self.send_json_response(404, {"error": "Caminho não encontrado."})

    def send_json_response(self, status_code, data):
        try:
            response_bytes = json.dumps(data).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response_bytes)
        except Exception as e:
            print(f"Erro ao enviar resposta no Vercel: {e}")
