# 📜 Game Design Document (GDD)

## 🎯 Visão Geral
**Cyber RPG** é um simulador de hacking tático que coloca o jogador no papel de um "Ghost Agent" infiltrando a rede da OmniCorp. O foco do jogo é o gerenciamento estratégico de três pilares: **Recursos (RAM)**, **Integridade (Conexão)** e **Visibilidade (Rastreio)**.

## ⚙️ Mecânicas de Elite

### 1. Gestão de Recursos (Core Loop)
- **RAM:** Limita o número de scripts que podem ser executados simultaneamente.
- **Trace (Rastreio):** Representa a proximidade da equipe de resposta (TI). Se atingir 100%, a conexão é terminada e o jogador perde o progresso (Game Over).
- **Estabilidade:** A "vida" do jogador. Ataques de defesa diminuem este valor.

### 2. Táticas de Hacking do Mundo Real (Avançado)
Implementamos mecânicas que simulam o cibercrime moderno:
- **Supply Chain Attack:** Infectar nós do tipo "Software Supplier". Após um timer de 4 turnos, o código malicioso se espalha para servidores OmniCorp conectados, garantindo acesso ROOT automático.
- **Social Engineering (Phishing):** Minijogo de diálogo com Personas (Estagiários, RH, TI). O sucesso depende da escolha da abordagem correta (técnica, urgente ou burocrática), permitindo bypass total de firewalls.
- **Zero-Day Exploit:** Mecânica de crafting. Jogadores coletam fragmentos de vulnerabilidade em servidores seguros para compilar um exploit de uso único que ignora qualquer defesa.
- **Ransomware & Extorsão Moderna:**
    - **Extorsão Dupla:** Opção de vazar dados para lucro imediato em troca de visibilidade extrema.
    - **Gestão de Tensão:** O rastreio aumenta drasticamente a cada turno enquanto o ransomware criptografa o alvo.

### 3. Agente Ghost (IA Mentora)
O comando secreto "...." ativa a IA que analisa a situação atual (nós, RAM, Trace) e toma a melhor decisão tática, explicando o raciocínio pedagógico por trás da ação.

## 🎭 Progressão e Economia
- **Missões:** Estruturadas via JSON, exigem a coleta de arquivos específicos para avançar na narrativa.
- **Mercado Negro:** Créditos obtidos via loot ou extorsão podem ser usados para comprar scripts mais potentes.
