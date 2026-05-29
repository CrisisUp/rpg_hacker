from ui import console
from entities.player import Player

class BlackMarket:
    """Sistema de loja para comprar upgrades (Dark Web)."""

    UPGRADES = [
        {"id": "ram_upgrade_1", "name": "Pente de RAM 8GB (DDR4)", "cost": 500, "type": "ram", "value": 8, "desc": "Aumenta a RAM máxima em 8GB."},
        {"id": "ram_upgrade_2", "name": "Módulo de RAM Quântica 16GB", "cost": 1200, "type": "ram", "value": 16, "desc": "Tecnologia experimental. +16GB RAM."},
        {"id": "trace_reducer_1", "name": "VPN Proxy Chain", "cost": 300, "type": "trace", "value": -20, "desc": "Reduz o rastreio atual em 20%."},
        {"id": "trace_reducer_2", "name": "Limpador de Logs de Elite", "cost": 800, "type": "trace", "value": -50, "desc": "Reduz o rastreio atual em 50%."},
    ]

    @classmethod
    def display_market(cls, player: Player):
        while True:
            console.console.clear()
            console.header("THE SILK ROAD", "MERCADO NEGRO DE HACKERS")
            console.console.print(f"[bold gold1]SEUS CRÉDITOS: ${player.credits}[/bold gold1]\n")
            
            for i, item in enumerate(cls.UPGRADES):
                status = "[bold green]DISPONÍVEL[/]" if player.credits >= item['cost'] else "[bold red]FUNDOS INSUFICIENTES[/]"
                console.console.print(f" [{i}] {item['name']} - [bold gold1]${item['cost']}[/] {status}")
                console.console.print(f"     [dim]{item['desc']}[/dim]\n")
            
            console.console.print(" [Q] Voltar ao Terminal")
            choice = console.ask("Selecione um item para comprar: ").upper()
            
            if choice == 'Q':
                break
            
            try:
                idx = int(choice)
                if 0 <= idx < len(cls.UPGRADES):
                    cls.buy_item(player, cls.UPGRADES[idx])
                else:
                    console.warning("Item inválido.")
                    console.wait_for_enter()
            except ValueError:
                pass

    @classmethod
    def buy_item(cls, player: Player, item: dict):
        if player.credits >= item['cost']:
            player.credits -= item['cost']
            
            if item['type'] == 'ram':
                player.max_ram += item['value']
                player.current_ram += item['value']
                console.success(f"Upgrade adquirido! RAM Máxima agora é {player.max_ram}GB.")
            elif item['type'] == 'trace':
                player.trace_level = max(0, player.trace_level + item['value'])
                console.success(f"Serviço adquirido! Rastreio reduzido para {player.trace_level}%.")
                
            from core.logger import AuditLogger
            AuditLogger.log("MERCADO", f"Comprou: {item['name']} por ${item['cost']}")
            
        else:
            console.error("Créditos insuficientes!")
        
        console.wait_for_enter()
