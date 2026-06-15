import requests

API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmZjg2YWNjLTNkOWQtNGYwYi1iZjE1LTdhNDdlOTYzODRjMiIsImlhdCI6MTc4MTQ3OTQwNCwic3ViIjoiZGV2ZWxvcGVyLzJiMjhiZWMxLWE4ZjEtODVjMC0yM2M0LTRhZjY2MDVkMTU2OSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTcwLjIzOS4xMTEuMTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.yRPlUGMchkXE1ZOdNQyrnudaMKn5nHrPIUALPJBTVXMH0FJ4XGVhk8uwgWC_FYMnQVU4f82-A3m6aVUjTidm-g"
PLAYER_TAG = "#RCG92GVJ"

formatted_tag = PLAYER_TAG.replace("#", "%23")
url = f"https://api.brawlstars.com/v1/players/{formatted_tag}/battlelog"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro na API: {response.status_code}")
        exit()
        
    partidas = response.json().get('items', [])
    
    total_partidas = len(partidas)
    vitorias = 0
    estatisticas_por_modo = {}

    for partida in partidas:
        detalhes = partida.get('battle', {})
        evento = partida.get('event', {})
        
        modo = evento.get('mode', 'Desconhecido').upper()
        mapa = evento.get('map', 'Desconhecido')
        
        # Inicializa o dicionário do modo para o relatório detalhado
        if modo not in estatisticas_por_modo:
            estatisticas_por_modo[modo] = {"partidas": 0, "vitorias": 0}
            
        estatisticas_por_modo[modo]["partidas"] += 1
        
        # Regra de Vitória do Solo Showdown (Top 4)
        if "SOLOSHOWDOWN" in modo:
            rank = detalhes.get('rank', 10)
            if rank <= 4:
                vitorias += 1
                estatisticas_por_modo[modo]["vitorias"] += 1
                
        # Regra de Vitória do Duo Showdown (Top 2)
        elif "DUOSHOWDOWN" in modo:
            rank = detalhes.get('rank', 5)
            if rank <= 2:
                vitorias += 1
                estatisticas_por_modo[modo]["vitorias"] += 1
                
        # Regra de Vitória para Modos 3v3
        else:
            resultado = detalhes.get('result', '')
            if resultado == "victory":
                vitorias += 1
                estatisticas_por_modo[modo]["vitorias"] += 1

    # Exibição dos Resultados (O "Coração" do seu futuro App)
    print("==================================================")
    print("       📊 ANÁLISE DE PERFORMANCE (LAST 25)       ")
    print("==================================================")
    
    win_rate_geral = (vitorias / total_partidas) * 100 if total_partidas > 0 else 0
    print(f"📈 Taxa de Vitória Geral: {win_rate_geral:.1f}% ({vitorias}/{total_partidas} partidas)")
    print("--------------------------------------------------")
    print("DESEMPENHO POR MODO:")
    
    for modo, dados in estatisticas_por_modo.items():
        wr_modo = (dados["vitorias"] / dados["partidas"]) * 100
        print(f"⚔️ {modo}: {wr_modo:.1f}% de vitórias ({dados['vitorias']}/{dados['partidas']})")
        
    print("==================================================")

except Exception as e:
    print(f"💥 Erro ao calcular: {e}")