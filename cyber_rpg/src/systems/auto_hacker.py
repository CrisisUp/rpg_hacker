import time
import random
from ui import console

class AutoHacker:
    """
    Agente de IA que analisa o estado do jogo e toma a melhor decisão.
    Funciona como um mentor pedagógico para o jogador.
    """
    
    @staticmethod
    def think(reason: str):
        """Simula o raciocínio da IA com efeito visual."""
        console.system("\n[bold magenta]『 SYSTEM OVERRIDE ATIVO 』[/bold magenta]")
        console.info(f"ANALISANDO: {reason}")
        time.sleep(1.5)

    @staticmethod
    def explain(action: str, logic: str):
        """Explica a decisão técnica tomada."""
        console.console.print(f"\n[bold yellow]↳ AÇÃO:[/bold yellow] [white]{action}[/white]")
        console.console.print(f"[bold cyan]↳ LÓGICA:[/bold cyan] [dim]{logic}[/dim]")
        time.sleep(2)

    @classmethod
    def resolve_navigation(cls, player, current_node, mission_manager):
        """Decide o próximo passo na rede."""
        cls.think("Topologia de rede e objetivos da missão")

        # Prioridade 1: Baixar arquivos se houver
        if current_node.data_files:
            cls.explain("Comando 'D'", "Sempre priorizamos a coleta de dados (Loot) antes de mover, para maximizar créditos e XP.")
            return 'D'

        # Prioridade 2: Procurar alvo da missão nas conexões
        target_file = mission_manager.active_mission.get('required_file') if mission_manager.active_mission else None
        for i, neighbor in enumerate(current_node.connections):
            if target_file and any(target_file in f for f in neighbor.data_files):
                cls.explain(f"Salto para {neighbor.ip}", f"Detectamos o arquivo alvo '{target_file}' neste nó. Iniciando aproximação direta.")
                return str(i)

        # Prioridade 3: Mover para o primeiro nó protegido para avançar na rede
        for i, neighbor in enumerate(current_node.connections):
            if not neighbor.is_hacked:
                cls.explain(f"Invasão em {neighbor.ip}", "Nó protegido detectado. Precisamos comprometer este sistema para expandir nosso alcance na rede.")
                return str(i)

        # Fallback: Salto aleatório para o primeiro vizinho
        cls.explain("Salto de Rota", "Nenhum alvo crítico imediato. Movendo para o próximo hop para mapear a rede.")
        return "0"

    @classmethod
    def resolve_combat(cls, hacker, server_health):
        """Decide a melhor estratégia de combate."""
        cls.think("Recursos de hardware e integridade do alvo")

        # Prioridade 1: Rastreio muito alto? Usar ProxyHop
        if hacker.trace_level > 70:
            proxy_idx = next((i for i, s in enumerate(hacker.scripts) if s.id == 'proxy_hop'), None)
            if proxy_idx is not None and hacker.current_ram >= 2:
                cls.explain("Script 'ProxyHop.v3'", "Nível de rastreio crítico (>70%). Priorizando ofuscação de IP para evitar desconexão forçada.")
                return "2", str(proxy_idx)

        # Prioridade 2: RAM baixa? Reiniciar
        if hacker.current_ram < 4:
            cls.explain("Ação 'Reboot'", "Memória RAM insuficiente para scripts de ataque. Reiniciando processos para recuperar poder de fogo.")
            return "3", None

        # Prioridade 3: Usar BruteForce ou SQLInject se tiver RAM
        best_attack = next((i for i, s in enumerate(hacker.scripts) if s.damage > 0), None)
        if best_attack is not None:
            script = hacker.scripts[best_attack]
            if hacker.current_ram >= script.ram_cost:
                cls.explain(f"Script '{script.name}'", f"Alvo possui {server_health} HP. Usando script de alto impacto para encerrar a invasão rapidamente.")
                return "2", str(best_attack)

        # Fallback: Ataque Manual
        cls.explain("Ataque Manual", "Economizando RAM. Usando injeção básica de pacotes para finalizar o alvo.")
        return "1", None
