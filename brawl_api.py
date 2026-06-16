import requests

class BrawlStarsClient:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.brawlstars.com/v1/players"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json"
        }

    def _format_tag(self, tag: str) -> str:
        # Garante que a tag comece com # e tira espaços
        tag = tag.strip()
        if not tag.startswith("#"):
            tag = f"#{tag}"
        # Formata para URL
        return tag.replace("#", "%23")

    def _normalize_tag(self, tag: str) -> str:
        tag = tag.strip()
        return tag if tag.startswith("#") else f"#{tag}"

    def get_player_data(self, player_tag: str) -> dict:
        formatted_tag = self._format_tag(player_tag)
        url = f"{self.base_url}/{formatted_tag}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_battle_log(self, player_tag: str) -> list:
        formatted_tag = self._format_tag(player_tag)
        url = f"{self.base_url}/{formatted_tag}/battlelog"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            response.raise_for_status()

    def get_complete_stats(self, player_tag: str) -> dict:
        player_tag_normalized = self._normalize_tag(player_tag)
        
        # 1. Busca dados do jogador
        player_data = self.get_player_data(player_tag)
        
        # 2. Busca histórico de batalhas
        partidas = self.get_battle_log(player_tag)
        
        # 3. Processamento das Estatísticas
        total_partidas = len(partidas)
        vitorias_gerais = 0
        estatisticas_por_modo = {}
        brawler_stats = {}
        historico_recente = []

        for partida in partidas:
            detalhes = partida.get('battle', {})
            evento = partida.get('event', {})
            
            modo = evento.get('mode', 'Desconhecido').upper()
            mapa = evento.get('map', 'Desconhecido')
            
            # Inicializa estatísticas por modo
            if modo not in estatisticas_por_modo:
                estatisticas_por_modo[modo] = {"partidas": 0, "vitorias": 0}
            estatisticas_por_modo[modo]["partidas"] += 1

            # Identificar brawler utilizado pelo jogador pesquisado
            brawler_usado = None
            brawler_id = None
            if 'players' in detalhes:
                for p in detalhes['players']:
                    if p.get('tag') == player_tag_normalized:
                        brawler_usado = p.get('brawler', {}).get('name', 'DESCONHECIDO')
                        brawler_id = p.get('brawler', {}).get('id')
                        break
            elif 'teams' in detalhes:
                for time in detalhes['teams']:
                    for p in time:
                        if p.get('tag') == player_tag_normalized:
                            brawler_usado = p.get('brawler', {}).get('name', 'DESCONHECIDO')
                            brawler_id = p.get('brawler', {}).get('id')
                            break

            # Se não achou o jogador, pula (improvável, mas possível)
            if not brawler_usado:
                brawler_usado = "DESCONHECIDO"

            if brawler_usado not in brawler_stats:
                brawler_stats[brawler_usado] = {"partidas": 0, "vitorias": 0, "id": brawler_id}
            brawler_stats[brawler_usado]["partidas"] += 1

            # Determinar vitória
            venceu = False
            resultado_status = ""
            if "SOLOSHOWDOWN" in modo:
                rank = detalhes.get('rank', 10)
                venceu = rank <= 4
                resultado_status = f"{rank}º Lugar"
            elif "DUOSHOWDOWN" in modo:
                rank = detalhes.get('rank', 5)
                venceu = rank <= 2
                resultado_status = f"{rank}º Lugar"
            else:
                resultado = detalhes.get('result', '')
                venceu = resultado == "victory"
                if resultado == "victory":
                    resultado_status = "Vitória"
                elif resultado == "defeat":
                    resultado_status = "Derrota"
                elif resultado == "draw":
                    resultado_status = "Empate"
                else:
                    resultado_status = resultado or "Desconhecido"

            if venceu:
                vitorias_gerais += 1
                estatisticas_por_modo[modo]["vitorias"] += 1
                brawler_stats[brawler_usado]["vitorias"] += 1

            # Adiciona ao histórico de partidas formatado para o front
            historico_recente.append({
                "modo": modo,
                "mapa": mapa,
                "brawler": brawler_usado,
                "resultado": resultado_status,
                "venceu": venceu
            })

        # Dicionário de Brawlers desbloqueados para consulta rápida
        unlocked_lookup = {b.get("name"): b for b in player_data.get("brawlers", [])}

        # Formata o win rate por modo
        resumo_modos = []
        for modo, dados in estatisticas_por_modo.items():
            wr = (dados["vitorias"] / dados["partidas"]) * 100 if dados["partidas"] > 0 else 0
            resumo_modos.append({
                "modo": modo,
                "partidas": dados["partidas"],
                "vitorias": dados["vitorias"],
                "winrate": round(wr, 1)
            })

        # Formata o win rate por brawler (apenas os jogados)
        resumo_brawlers = []
        for brawler, dados in brawler_stats.items():
            wr = (dados["vitorias"] / dados["partidas"]) * 100 if dados["partidas"] > 0 else 0
            b_info = unlocked_lookup.get(brawler, {})
            brawler_id = dados.get("id") or b_info.get("id")
            resumo_brawlers.append({
                "id": brawler_id,
                "brawler": brawler,
                "partidas": dados["partidas"],
                "vitorias": dados["vitorias"],
                "winrate": round(wr, 1),
                "trophies": b_info.get("trophies", 0),
                "power": b_info.get("power", 1)
            })
        # Ordena por mais partidas jogadas
        resumo_brawlers = sorted(resumo_brawlers, key=lambda x: x["partidas"], reverse=True)

        # Processa a lista completa de todos os brawlers desbloqueados com seus troféus e níveis
        brawlers_todos = []
        for b in player_data.get("brawlers", []):
            brawlers_todos.append({
                "id": b.get("id"),
                "brawler": b.get("name", "DESCONHECIDO"),
                "power": b.get("power", 1),
                "trophies": b.get("trophies", 0),
                "highestTrophies": b.get("highestTrophies", 0)
            })
        # Ordena todos os brawlers por troféus (do maior para o menor)
        brawlers_todos = sorted(brawlers_todos, key=lambda x: x["trophies"], reverse=True)

        winrate_geral = (vitorias_gerais / total_partidas) * 100 if total_partidas > 0 else 0

        # Retorna o payload completo estruturado
        return {
            "player": {
                "name": player_data.get("name"),
                "tag": player_tag_normalized,
                "trophies": player_data.get("trophies"),
                "highestTrophies": player_data.get("highestTrophies"),
                "expLevel": player_data.get("expLevel"),
                "victories3v3": player_data.get("3vs3Victories"),
                "brawlersUnlocked": len(player_data.get("brawlers", []))
            },
            "stats": {
                "total": total_partidas,
                "vitorias": vitorias_gerais,
                "winrate": round(winrate_geral, 1)
            },
            "modos": resumo_modos,
            "brawlers": resumo_brawlers,
            "brawlers_todos": brawlers_todos,
            "historico": historico_recente
        }
