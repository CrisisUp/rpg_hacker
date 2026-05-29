# 🏗️ Arquitetura Técnica

## 📐 Princípios Aplicados

- **SRP:** GameLoop, MissionManager, StateManager e UI isolados.
- **Dataclasses:** Tipagem forte em \`entities/script.py\`.
- **Abstração de I/O:** Camada UI desacoplada da lógica de negócio.

## 🧪 Testes

Validamos Lógica de Grafo, Raciocínio da IA e Integridade de Save.

## 🔄 Fluxo

main.py -> GameLoop -> MissionManager -> Generator -> Rich UI
