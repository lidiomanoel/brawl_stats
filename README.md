# ⚔️ Brawl Stats - Dashboard de Performance

Um dashboard da web moderno, responsivo e interativo para consultar e analisar estatísticas de jogadores do **Brawl Stars** em tempo real usando a API oficial da Supercell.

---

## 🚀 Funcionalidades

- **Busca por Tag**: Insira qualquer tag de jogador do Brawl Stars para buscar dados dinamicamente.
- **Resumo do Perfil**: Visualização instantânea de troféus atuais, recorde histórico, nível de XP e quantidade de Brawlers liberados.
- **Taxa de Vitória Geral**: Cálculo do *win rate* baseado nos últimos 25 combates do jogador, representado graficamente por um anel de progresso SVG animado.
- **Histórico Recente**: Feed das últimas partidas detalhando o modo de jogo, mapa jogado, brawler utilizado e o resultado (vitória, derrota, empate ou posição no Showdown).
- **Aba de Brawlers Interativa**:
  - **🎯 Eficiência**: Lista os Brawlers utilizados nas partidas recentes com a respectiva taxa de vitória, troféus e nível de poder.
  - **🏆 Troféus**: Lista completa de todos os Brawlers desbloqueados pelo jogador, ordenados do maior número de troféus para o menor, com barras de progresso visuais e recordes individuais.
- **Performance Otimizada**: Sistema de abas com cache de dados no cliente para evitar chamadas de API desnecessárias.

---

## 🛠️ Tecnologias Utilizadas

- **Back-end (Python)**:
  - Consumo da API oficial do Brawl Stars com a biblioteca `requests`.
  - Servidor HTTP nativo com o módulo padrão `http.server`.
- **Front-end (Web)**:
  - **HTML5**: Estrutura semântica dos elementos.
  - **CSS3 (Moderno)**: Efeitos de *glassmorphism* (cartões translúcidos), orbes de luz pulsantes em segundo plano, animações de transição e barras de rolagem customizadas.
  - **JavaScript (ES6+)**: Manipulação dinâmica do DOM, requisições assíncronas (Fetch API) e cálculo de SVG stroke-dash para o gráfico de vitórias.

---

## 💻 Como Rodar o Projeto Localmente

### Pré-requisitos
Certifique-se de ter o **Python 3** instalado em sua máquina.

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/brawl-stats-app.git
   cd brawl-stats-app
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o servidor local**:
   ```bash
   python server.py
   ```

4. **Acesse no seu navegador**:
   Abra [http://localhost:8000](http://localhost:8000)

---

## ☁️ Como Hospedar e Compartilhar

Preparamos guias detalhados para te ajudar a colocar o projeto online de graça:
- **Para hospedagem geral (Render, Railway, VPS, etc.)**: Leia o guia **[COMO_HOSPEDAR.md](COMO_HOSPEDAR.md)**.
- **Para hospedagem rápida na Vercel (Serverless)**: Leia o guia **[COMO_VERCEL.md](COMO_VERCEL.md)**.
- **Para aprender a enviar atualizações**: Leia o guia **[COMO_ATUALIZAR.md](COMO_ATUALIZAR.md)**.

---

## ⚠️ Isenção de Responsabilidade

Este aplicativo não é afiliado, endossado, patrocinado ou aprovado especificamente pela Supercell. A Supercell não é responsável por seu funcionamento. Para obter mais informações, consulte a Política de Conteúdo para Fãs da Supercell.
