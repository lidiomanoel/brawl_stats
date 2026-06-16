import http.server
import socketserver
import urllib.parse
import json
import traceback
import sys
import os

from brawl_api import BrawlStarsClient

# Token da API obtido dos seus scripts de teste
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmZjg2YWNjLTNkOWQtNGYwYi1iZjE1LTdhNDdlOTYzODRjMiIsImlhdCI6MTc4MTQ3OTQwNCwic3ViIjoiZGV2ZWxvcGVyLzJiMjhiZWMxLWE4ZjEtODVjMC0yM2M0LTRhZjY2MDVkMTU2OSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTcwLjIzOS4xMTEuMTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.yRPlUGMchkXE1ZOdNQyrnudaMKn5nHrPIUALPJBTVXMH0FJ4XGVhk8uwgWC_FYMnQVU4f82-A3m6aVUjTidm-g"
PORT = int(os.environ.get("PORT", 8000))
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))

client = BrawlStarsClient(API_TOKEN)

class BrawlStarsServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Define a pasta de onde servirá os arquivos estáticos
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Intercepta a chamada de API
        if path == "/api/stats":
            query_params = urllib.parse.parse_qs(parsed_url.query)
            tag = query_params.get("tag", [""])[0]
            
            if not tag:
                self.send_error_response(400, "A tag do jogador é obrigatória.")
                return
                
            try:
                # Busca as estatísticas consolidadas
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
                    msg = "Erro de autenticação (Chave de API expirada ou IP não autorizado)."
                self.send_error_response(status, msg)
        else:
            # Caso contrário, serve arquivos estáticos (HTML, CSS, JS)
            super().do_GET()

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
            print(f"Erro ao enviar resposta JSON: {e}")

    def send_error_response(self, status_code, message):
        data = {"error": message}
        self.send_json_response(status_code, data)

def run_server():
    # Cria a pasta frontend se ela não existir
    if not os.path.exists(FRONTEND_DIR):
        os.makedirs(FRONTEND_DIR)
        
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), BrawlStarsServerHandler) as httpd:
        print(f"🚀 Servidor rodando em http://localhost:{PORT}")
        print(f"📁 Servindo arquivos de: {FRONTEND_DIR}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Servidor encerrado.")
            sys.exit(0)

if __name__ == "__main__":
    run_server()
