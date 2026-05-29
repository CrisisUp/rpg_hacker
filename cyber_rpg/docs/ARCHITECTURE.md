# 🏗️ Arquitetura Técnica

O projeto segue princípios de Clean Code e Arquitetura Orientada a Eventos/Estados.

## 📐 Estrutura de Camadas

1.  **Entidades (src/entities/):** Objetos puros como Player, NetworkNode e Script. Possuem estado e lógica interna, mas não conhecem a UI ou o Loop Global.
2.  **Sistemas (src/systems/):** Motores de lógica.
    *   combat.py: Gerencia o estado de invasão de um nó.
    *   generator.py: Algoritmos de geração procedural de grafos de rede.
    *   missions.py: Gerenciador de objetivos e progressão narrativa.
3.  **Core (src/core/):**
    *   game_loop.py: O orquestrador central. Gerencia ações passivas por turno (MITM, XSS, Ransomware, Supply Chain).
    *   state.py: Camada de persistência (JSON).
4.  **UI (src/ui/):** Abstração visual usando a biblioteca Rich.

## 🔄 Mecânicas de Segundo Plano (Passive Actions)
O jogo utiliza um sistema de processamento passivo no Loop Principal:
*   **Tick System:** A cada ação do jogador, o loop processa timers ativos em todos os nós da rede.
*   **Cascade Effect:** Mecânicas como Supply Chain injetam eventos em nós adjacentes no grafo de rede baseado em condições de timer.

## 🧪 Testes e Qualidade
*   **Testes Unitários:** Focados em entidades e cálculos de dano/recursos.
*   **Testes de Integração:** Validam mecânicas complexas como o efeito cascata do Supply Chain e compilação de Zero-Days.
