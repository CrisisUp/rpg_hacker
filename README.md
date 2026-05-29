# 🌐 RPG Hacker: Cyberpunk Terminal Simulator

Um simulador de hacking tático via terminal, onde você assume o papel do **Agente Ghost**. O jogo foi construído com foco em **Táticas Reais de Hacking**, **Narrativa Ramificada** e uma arquitetura robusta baseada nos princípios do **Clean Code** e **SOLID**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Rich](https://img.shields.io/badge/UI-Rich_Terminal-magenta)

## 🚀 Funcionalidades e Mecânicas

### 🕹️ Gameplay Dinâmico

- **Mercado Negro (Dark Web):** Economia de créditos onde você pode comprar upgrades de hardware (RAM Quântica) e serviços de limpeza de rastro (VPN Proxy Chain).
- **Notoriedade e IAs Hunters:** O mundo reage à sua fama. Concluir missões (especialmente de forma barulhenta) aumenta sua Notoriedade, atraindo ataques surpresa de "Hunters" (IAs de contra-inteligência).
- **Contra-medidas Dinâmicas (ICE):** Durante tentativas de invasão, os servidores inimigos reagem aos seus ataques, podendo recuperar HP, aumentar seu Rastreio ou sabotar sua Estabilidade de Conexão.
- **Hacker Rival (Zero_Cool):** Um rival dinâmico que navega pela mesma rede, roubando arquivos preciosos antes de você. Intercepte-o para recuperar os dados em combates mais difíceis!
- **Engenharia Social Interativa:** Um minijogo de Phishing com diálogos ramificados adaptados a diferentes personas (Estagiários, SysAdmins exaustos, CEOs em viagem).

### 📖 Narrativa Profunda

- **Lore Funcional:** Os arquivos baixados (logs, e-mails, notas criptografadas) contêm dicas reais de senhas, vulnerabilidades e nós secretos escondidos na rede.
- **Múltiplos Finais:** Suas escolhas durante as missões e seu nível final de Notoriedade definem o desfecho da história ao recuperar o "Projeto Alpha" (Lealdade ao Architect, Vazamento Público ou Apagar Rastro).
- **E-mails Reativos:** A sua *Inbox* recebe mensagens contextuais não apenas do seu contratante, mas também de inimigos e informantes anônimos de acordo com seu progresso e fama.

### 🛠️ Arsenal Hacker

- **Supply Chain Attack:** Infiltre-se em fornecedores para comprometer alvos corporativos de forma indireta.
- **Zero-Day Crafting:** Colete fragmentos pela rede para compilar exploits massivos de uso único.
- **Ransomware de Extorsão Dupla:** Criptografe servidores e escolha entre extorsão silenciosa ou vazar dados para lucrar alto (mas alertar a corporação).

## 💻 Instalação e Execução

O jogo utiliza a biblioteca `rich` para fornecer uma interface gráfica incrível baseada em texto diretamente no seu terminal.

```bash
# 1. Clone o repositório
git clone https://github.com/CrisisUp/rpg_hacker.git
cd rpg_hacker

# 2. Crie e ative um ambiente virtual (Recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r cyber_rpg/requirements.txt

# 4. Rode o jogo
python cyber_rpg/src/main.py
```

## 🧪 Testes Automatizados

O projeto conta com uma robusta suíte de testes unitários validando as lógicas de combate, estado, phishing e efeitos de script.

```bash
# Com o ambiente virtual ativado:
pytest cyber_rpg/tests/
```

## 🏗️ Arquitetura e Clean Code

Este projeto foi severamente refatorado para aderir a boas práticas de Engenharia de Software:

- **Padrão Dispatch (Command Pattern):** Substituição de "Arrow Code" e encadeamentos infinitos de `if/else` por dicionários de roteamento.
- **Princípio da Responsabilidade Única (SRP):** Lógicas de UI, Orquestração (GameLoop) e Sessões de Combate estritamente separadas.
- **Princípio Aberto-Fechado (OCP):** Scripts de efeitos e cenários narrativos extraídos para arquivos de configuração e dados externos (`JSON`), tornando o jogo escalável sem necessidade de alterar o código principal Python.
- **Design Patterns aplicados:** Singleton (Cache de efeitos), Strategy/Command (Menus e Combate) e Delegação.

---
*Desenvolvido em colaboração com o Agente Ghost.*
