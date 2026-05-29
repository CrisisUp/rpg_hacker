from ui import console

class CombatUI:
    """Centraliza todas as interações visuais e entradas durante o combate."""
    
    @staticmethod
    def display_header(target_ip):
        console.header(f"INICIANDO INVASÃO: {target_ip}")

    @staticmethod
    def display_status(hacker, server_health):
        print(f"\n[ALVO]: {server_health} HP | [CONEXÃO]: {hacker.connection_stability}% | [RAM]: {hacker.current_ram}GB")
        console.trace_bar(hacker.trace_level)
        print("\n[1] Ataque Manual | [2] Usar Script | [3] Reboot")

    @staticmethod
    def ask_action():
        return console.ask("Ação [1-3]: ")

    @staticmethod
    def ask_manual_cmd(cmd):
        console.info(f" >>> DIGITE RÁPIDO: {cmd}")
        return console.ask("> ")

    @staticmethod
    def display_script_menu(scripts):
        for i, s in enumerate(scripts):
            print(f" [{i}] {s.name} ({s.ram_cost}GB)")
        return console.ask("Índice (V para voltar): ").upper()

    @staticmethod
    def display_privesc_challenge(addresses):
        console.header("PRIVILEGE ESCALATION", "SCANNING FOR KERNEL EXPLOITS")
        for i, addr in enumerate(addresses):
            print(f" [{i}] {addr}")
        return console.ask("Endereço (terminado em 0): ")
