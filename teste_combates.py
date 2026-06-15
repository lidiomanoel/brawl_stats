import requests

# Seus dados de autenticação
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmZjg2YWNjLTNkOWQtNGYwYi1iZjE1LTdhNDdlOTYzODRjMiIsImlhdCI6MTc4MTQ3OTQwNCwic3ViIjoiZGV2ZWxvcGVyLzJiMjhiZWMxLWE4ZjEtODVjMC0yM2M0LTRhZjY2MDVkMTU2OSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTcwLjIzOS4xMTEuMTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.yRPlUGMchkXE1ZOdNQyrnudaMKn5nHrPIUALPJBTVXMH0FJ4XGVhk8uwgWC_FYMnQVU4f82-A3m6aVUjTidm-g"
PLAYER_TAG = "#RCG92GVJ"

formatted_tag = PLAYER_TAG.replace("#", "%23")
# Mudamos o endpoint para focar no histórico de batalhas
url = f"https://api.brawlstars.com/v1/players/{formatted_tag}/battlelog"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

print("🔄 Buscando seus últimos combates...\n")

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        log_data = response.json()
        partidas = log_data.get('items', [])
        
        print(f"✅ Encontradas {len(partidas)} partidas recentes.\n")
        print("📊 HISTÓRICO RECENTE:")
        print("-" * 50)
        
        for idx, partida in enumerate(partidas[:10], start=1): # Mostra as 10 últimas
            detalhes = partida.get('battle', {})
            evento = partida.get('event', {})
            
            modo = evento.get('mode', 'Desconhecido')
            mapa = evento.get('map', 'Desconhecido')
            
            # O resultado pode vir como 'result' (victory/defeat) ou 'rank' (em modos Showdown)
            resultado = detalhes.get('result')
            rank_showdown = detalhes.get('rank')
            
            if resultado:
                status = "🟢 VITÓRIA" if resultado == "victory" else "🔴 DERROTA"
                if resultado == "draw": status = "🟡 EMPATE"
            elif rank_showdown:
                status = f"🤠 Posição: {rank_showdown}º Lugar"
            else:
                status = "❓ Sem resultado claro"
                
            print(f"{idx}. Modo: {modo.upper()} | Mapa: {mapa}")
            print(f"   Resultado: {status}")
            print("-" * 50)
            
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")

except Exception as e:
    print(f"💥 Erro: {e}")