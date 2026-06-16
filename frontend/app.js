document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("search-form");
    const tagInput = document.getElementById("tag-input");
    const searchBtn = document.getElementById("search-btn");
    
    const loader = document.getElementById("loader");
    const errorCard = document.getElementById("error-card");
    const errorMessage = document.getElementById("error-message");
    const dashboard = document.getElementById("dashboard");
    
    // Elementos do perfil do jogador
    const playerName = document.getElementById("player-name");
    const playerTag = document.getElementById("player-tag");
    const statTrophies = document.getElementById("stat-trophies");
    const statHighest = document.getElementById("stat-highest");
    const statXp = document.getElementById("stat-xp");
    const statBrawlers = document.getElementById("stat-brawlers");
    
    // Elementos da Taxa de Vitória
    const winrateRing = document.getElementById("winrate-ring");
    const winrateValue = document.getElementById("winrate-value");
    const statsWins = document.getElementById("stats-wins");
    const statsLosses = document.getElementById("stats-losses");
    const winrateFeedback = document.getElementById("winrate-feedback");
    
    // Contêineres e Abas de listagens
    const brawlerListContainer = document.getElementById("brawler-list-container");
    const historyListContainer = document.getElementById("history-list-container");
    const tabPlayedBtn = document.getElementById("tab-played");
    const tabAllBtn = document.getElementById("tab-all");
    
    // Dados globais do jogador atualmente carregado
    let currentData = null;
    let currentTab = "played"; // "played" ou "all"
    
    // Circunferência do anel de progresso (2 * PI * R) -> 2 * 3.14159 * 68 = 427.26
    const RING_CIRCUMFERENCE = 427.26;
    
    // Configura o anel de progresso inicialmente vazio
    winrateRing.style.strokeDasharray = `${RING_CIRCUMFERENCE} ${RING_CIRCUMFERENCE}`;
    winrateRing.style.strokeDashoffset = RING_CIRCUMFERENCE;

    // Busca automática inicial da Tag padrão ao abrir
    fetchPlayerStats("RCG92GVJ");

    // Evento de Submit da Busca
    searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const tag = tagInput.value.trim().replace("#", "");
        if (tag) {
            fetchPlayerStats(tag);
        }
    });

    // Eventos de troca de aba
    tabPlayedBtn.addEventListener("click", () => {
        if (currentTab === "played") return;
        currentTab = "played";
        tabPlayedBtn.classList.add("active");
        tabAllBtn.classList.remove("active");
        renderBrawlerList();
    });

    tabAllBtn.addEventListener("click", () => {
        if (currentTab === "all") return;
        currentTab = "all";
        tabAllBtn.classList.add("active");
        tabPlayedBtn.classList.remove("active");
        renderBrawlerList();
    });

    async function fetchPlayerStats(tag) {
        showLoader();
        try {
            const response = await fetch(`/api/stats?tag=${encodeURIComponent(tag)}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `Erro do servidor (${response.status})`);
            }
            
            currentData = data;
            renderDashboard();
        } catch (error) {
            showError(error.message);
        }
    }

    function renderDashboard() {
        if (!currentData) return;
        
        // 1. Dados Básicos do Perfil
        playerName.textContent = currentData.player.name;
        playerTag.textContent = currentData.player.tag;
        statTrophies.textContent = currentData.player.trophies.toLocaleString('pt-BR');
        statHighest.textContent = currentData.player.highestTrophies.toLocaleString('pt-BR');
        statXp.textContent = currentData.player.expLevel;
        statBrawlers.textContent = currentData.player.brawlersUnlocked;
        
        // Atualiza os botões das abas com contagens
        tabAllBtn.textContent = `🏆 TODOS (${currentData.player.brawlersUnlocked})`;
        
        // 2. Anel de Taxa de Vitória e Detalhes
        const winrate = currentData.stats.winrate;
        const total = currentData.stats.total;
        const wins = currentData.stats.vitorias;
        const losses = total - wins;
        
        winrateValue.textContent = `${winrate}%`;
        statsWins.textContent = wins;
        statsLosses.textContent = losses;
        
        // Atualiza a barra/anel usando dashoffset
        const offset = RING_CIRCUMFERENCE - (winrate / 100) * RING_CIRCUMFERENCE;
        winrateRing.style.strokeDashoffset = offset;
        
        // Feedback Text
        let feedback = "Bom";
        if (winrate >= 80) {
            feedback = "Lendário! 👑";
        } else if (winrate >= 70) {
            feedback = "Excelente! 🔥";
        } else if (winrate >= 55) {
            feedback = "Muito Bom! 👍";
        } else if (winrate >= 40) {
            feedback = "Razoável! ⚔️";
        } else {
            feedback = "Pode Melhorar! 💪";
        }
        winrateFeedback.textContent = feedback;
        
        // 3. Renderizar Lista de Brawlers (Baseado na aba ativa)
        renderBrawlerList();
        
        // 4. Renderizar Histórico de Partidas
        historyListContainer.innerHTML = "";
        if (currentData.historico && currentData.historico.length > 0) {
            currentData.historico.forEach(match => {
                const matchDiv = document.createElement("div");
                
                // Determina classe de estilo de acordo com o resultado
                let statusClass = "history-draw";
                let badgeClass = "res-draw";
                
                const res = match.resultado.toUpperCase();
                
                if (match.venceu || res.includes("VITÓRIA") || res === "1º LUGAR" || res === "2º LUGAR" || res === "3º LUGAR" || res === "4º LUGAR") {
                    statusClass = "history-victory";
                    badgeClass = "res-win";
                } else if (res.includes("DERROTA") || res === "5º LUGAR" || res === "6º LUGAR" || res === "7º LUGAR" || res === "8º LUGAR" || res === "9º LUGAR" || res === "10º LUGAR") {
                    statusClass = "history-defeat";
                    badgeClass = "res-lose";
                }
                
                if (res.includes("LUGAR")) {
                    badgeClass = "res-rank";
                }
                
                matchDiv.className = `history-item ${statusClass}`;
                
                // Tradução amigável do modo
                let modoDisplay = match.modo.replace("SOLOSHOWDOWN", "Solo Showdown").replace("DUOSHOWDOWN", "Duo Showdown");
                modoDisplay = modoDisplay.charAt(0) + modoDisplay.slice(1).toLowerCase();
                
                matchDiv.innerHTML = `
                    <div class="history-match-info">
                        <div class="history-mode-map">
                            ${modoDisplay}
                            <span>${match.mapa}</span>
                        </div>
                        <div class="history-brawler">
                            <span>Brawler: <strong>${match.brawler}</strong></span>
                        </div>
                    </div>
                    <span class="history-result-badge ${badgeClass}">${match.resultado}</span>
                `;
                historyListContainer.appendChild(matchDiv);
            });
        } else {
            historyListContainer.innerHTML = `<p class="subtitle" style="text-align: center;">Nenhum combate registrado.</p>`;
        }
        
        showDashboard();
    }

    function renderBrawlerList() {
        if (!currentData) return;
        
        brawlerListContainer.innerHTML = "";
        
        if (currentTab === "played") {
            // ABA: Eficiência nas partidas recentes
            if (currentData.brawlers && currentData.brawlers.length > 0) {
                currentData.brawlers.forEach(item => {
                    const brawlerDiv = document.createElement("div");
                    brawlerDiv.className = "brawler-item";
                    
                    let wrClass = "win-mid";
                    if (item.winrate >= 65) wrClass = "win-high";
                    else if (item.winrate < 50) wrClass = "win-low";
                    
                    brawlerDiv.innerHTML = `
                        <div class="brawler-icon-box">🤠</div>
                        <div class="brawler-info-col">
                            <div class="brawler-name-row">
                                <span class="brawler-name">${item.brawler}</span>
                                <span class="brawler-games">${item.partidas} ${item.partidas === 1 ? 'partida' : 'partidas'}</span>
                            </div>
                            <div class="brawler-bar-bg">
                                <div class="brawler-bar-fill" style="width: ${item.winrate}%"></div>
                            </div>
                            <div class="brawler-name-row" style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: normal; margin-top: 0.15rem;">
                                <span>🏆 ${item.trophies} | Poder ${item.power}</span>
                            </div>
                        </div>
                        <span class="brawler-winrate-badge ${wrClass}">${item.winrate}%</span>
                    `;
                    brawlerListContainer.appendChild(brawlerDiv);
                });
            } else {
                brawlerListContainer.innerHTML = `<p class="subtitle" style="text-align: center;">Nenhum Brawler jogado recentemente.</p>`;
            }
        } else {
            // ABA: Todos os Brawlers com seus Troféus
            if (currentData.brawlers_todos && currentData.brawlers_todos.length > 0) {
                currentData.brawlers_todos.forEach(item => {
                    const brawlerDiv = document.createElement("div");
                    brawlerDiv.className = "brawler-item";
                    
                    // Progresso visual baseado em 1000 troféus
                    const fillPercent = Math.min((item.trophies / 1000) * 100, 100);
                    
                    // Define classe de badge baseada nos troféus para dar um visual legal
                    let trophyClass = "win-low";
                    if (item.trophies >= 750) trophyClass = "win-high"; // Alta performance
                    else if (item.trophies >= 500) trophyClass = "win-mid"; // Média performance
                    
                    brawlerDiv.innerHTML = `
                        <div class="brawler-icon-box" style="background: var(--grad-gold); color: #000;">🌵</div>
                        <div class="brawler-info-col">
                            <div class="brawler-name-row">
                                <span class="brawler-name">${item.brawler}</span>
                                <span class="brawler-games" style="color: var(--color-text-muted);">Poder ${item.power}</span>
                            </div>
                            <div class="brawler-bar-bg">
                                <div class="brawler-bar-fill" style="width: ${fillPercent}%; background: var(--grad-purple)"></div>
                            </div>
                            <div class="brawler-name-row" style="font-size: 0.75rem; color: var(--color-text-muted); font-weight: normal; margin-top: 0.15rem;">
                                <span>Recorde: 🏆 ${item.highestTrophies}</span>
                            </div>
                        </div>
                        <span class="brawler-winrate-badge ${trophyClass}" style="display: flex; align-items: center; gap: 0.25rem;">
                            🏆 ${item.trophies}
                        </span>
                    `;
                    brawlerListContainer.appendChild(brawlerDiv);
                });
            } else {
                brawlerListContainer.innerHTML = `<p class="subtitle" style="text-align: center;">Nenhum Brawler liberado.</p>`;
            }
        }
    }

    function showLoader() {
        loader.classList.remove("hidden");
        errorCard.classList.add("hidden");
        dashboard.classList.add("hidden");
        searchBtn.disabled = true;
    }

    function showDashboard() {
        loader.classList.add("hidden");
        errorCard.classList.add("hidden");
        dashboard.classList.remove("hidden");
        searchBtn.disabled = false;
    }

    function showError(msg) {
        loader.classList.add("hidden");
        dashboard.classList.add("hidden");
        errorMessage.textContent = msg;
        errorCard.classList.remove("hidden");
        searchBtn.disabled = false;
    }
});
