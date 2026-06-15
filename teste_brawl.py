import requests
import json

# ==========================================
# INSIRA SEUS DADOS AQUI
# ==========================================
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmZjg2YWNjLTNkOWQtNGYwYi1iZjE1LTdhNDdlOTYzODRjMiIsImlhdCI6MTc4MTQ3OTQwNCwic3ViIjoiZGV2ZWxvcGVyLzJiMjhiZWMxLWE4ZjEtODVjMC0yM2M0LTRhZjY2MDVkMTU2OSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTcwLjIzOS4xMTEuMTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.yRPlUGMchkXE1ZOdNQyrnudaMKn5nHrPIUALPJBTVXMH0FJ4XGVhk8uwgWC_FYMnQVU4f82-A3m6aVUjTidm-g"
PLAYER_TAG = "#RCG92GVJ"
# ==========================================

# Trata a Tag para o formato que a API aceita (substitui # por %23)
formatted_tag = PLAYER_TAG.replace("#", "%23")
url = f"https://api.brawlstars.com/v1/players/{formatted_tag}"

# Cabeçalhos obrigatórios para autenticação
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

print(f"🔄 Conectando à API do Brawl Stars para buscar a tag {PLAYER_TAG}...\n")

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        player_data = response.json()
        
        # Exibe um resumo estruturado dos dados da sua conta
        print("✅ Conexão estabelecida com sucesso!\n")
        print(f"👤 Nome do Jogador: {player_data.get('name')}")
        print(f"🏆 Troféus Atuais: {player_data.get('trophies')}")
        print(f"🥇 Recorde de Troféus: {player_data.get('highestTrophies')}")
        print(f"⭐ Nível de XP: {player_data.get('expLevel')}")
        print(f"⚔️ Vitórias 3v3: {player_data.get('3vs3Victories')}")
        print(f"🌵 Total de Brawlers Liberados: {len(player_data.get('brawlers', []))}")
        
        print("\n--- Exemplo de dados de um Brawler seu ---")
        if player_data.get('brawlers'):
            primeiro_brawler = player_data['brawlers'][0]
            print(f"Brawler: {primeiro_brawler.get('name')}")
            print(f"Poder: {primeiro_brawler.get('power')}")
            print(f"Troféus com ele: {primeiro_brawler.get('trophies')}")
            
    elif response.status_code == 403:
        print("❌ Erro 403: Acesso negado!")
        print("Verifique se o IP cadastrado na chave do portal do desenvolvedor é exatamente o mesmo da sua máquina atual.")
    elif response.status_code == 404:
        print("❌ Erro 404: Jogador não encontrado. Verifique se digitou a Tag corretamente.")
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")

except Exception as e:
    print(f"💥 Ocorreu um erro inesperado: {e}")