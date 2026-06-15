import requests

API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmZjg2YWNjLTNkOWQtNGYwYi1iZjE1LTdhNDdlOTYzODRjMiIsImlhdCI6MTc4MTQ3OTQwNCwic3ViIjoiZGV2ZWxvcGVyLzJiMjhiZWMxLWE4ZjEtODVjMC0yM2M0LTRhZjY2MDVkMTU2OSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTcwLjIzOS4xMTEuMTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.yRPlUGMchkXE1ZOdNQyrnudaMKn5nHrPIUALPJBTVXMH0FJ4XGVhk8uwgWC_FYMnQVU4f82-A3m6aVUjTidm-g"
PLAYER_TAG = "#RCG92GVJ"

# Normaliza a tag para busca no JSON (mantendo o # se houver)
PLAYER_TAG_NORMALIZED = PLAYER_TAG if PLAYER_TAG.startswith("#") else f"#{PLAYER_TAG}"

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
    brawler_stats = {}

    for partida in partidas:
        detalhes = partida.get('battle', {})
        evento = partida.get('event', {})
        modo = evento.get('mode', 'Desconhecido').upper()
        
        # Encontra qual Brawler VOCÊ usou na partida
        brawler_usado = None
        
        # No Solo/Duo Showdown os jogadores ficam na lista 'players'
        if 'players' in detalhes:
            for p in detalhes['players']:
                if p.get('tag') == PLAYER_TAG_NORMALIZED:
                    brawler_usado = p.get('brawler', {}).get('name', 'DESCONHECIDO')
                    break
        # Nos modos 3v3 os jogadores ficam divididos em 'teams'
        elif 'teams' in detalhes:
            for time in detalhes['teams']:
                for p in time:
                    if p.get('tag') == PLAYER_TAG_NORMALIZED:
                        brawler_usado = p.get('brawler', {}).get('name', 'DESCONHECIDO')
                        break
        
        if not brawler_usado:
            continue # Se não achou o jogador, pula para a próxima
            
        # Inicializa o Brawler no dicionário de estatísticas
        if brawler_usado not in brawler_stats:
            brawler_stats[brawler_usado] = {"partidas": 0, "vitorias": 0}
            
        brawler_stats[brawler_usado]["partidas"] += 1
        
        # Aplica a regra de vitória para contabilizar o Brawler
        venceu = False
        if "SOLOSHOWDOWN" in modo:
            venceu = detalhes.get('rank', 10) <= 4
        elif "DUOSHOWDOWN" in modo:
            venceu = detalhes.get('rank', 5) <= 2
        else:
            venceu = detalhes.get('result', '') == "victory"
            
        if venceu:
            brawler_stats[brawler_usado]["vitorias"] += 1

    # Exibição dos Insights de Desempenho
    print("==================================================")
    print("      🎯 WIN RATE DETALHADO POR BRAWLER          ")
    print("==================================================")
    
    # Ordena os brawlers pelo maior número de partidas jogadas
    brawlers_ordenados = sorted(brawler_stats.items(), key=lambda x: x[1]['partidas'], reverse=True)
    
    for brawler, dados in brawlers_ordenados:
        wr = (dados["vitorias"] / dados["partidas"]) * 100
        print(f"🤠 {brawler.upper():<12} | Qtd: {dados['partidas']:<2} | Win Rate: {wr:.1f}%")
        
    print("==================================================")

except Exception as e:
    print(f"💥 Erro ao processar brawlers: {e}")