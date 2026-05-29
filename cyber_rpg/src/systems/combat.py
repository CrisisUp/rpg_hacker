import random
import time
from ui import console
from entities.player import Player
from entities.network import NetworkNode
from entities.script import HackingScript
from systems.auto_hacker import AutoHacker

def start_hack(hacker: Player, target_server: NetworkNode) -> bool:
    """Invasão inicial para ganhar acesso USER."""
    console.header(f"INVASÃO INICIAL: {target_server.ip}")
    server_health = 40 if "Firewall" in target_server.node_type else 25
    
    while server_health > 0 and hacker.connection_stability > 0:
        _display_combat_status(hacker, server_health)
        player_choice = console.ask("Ação [1-3] ou '....': ")

        if player_choice == "....":
            action, sub_action = AutoHacker.resolve_combat(hacker, server_health)
            if action == "1": server_health -= _process_manual_attack(hacker, auto=True)
            elif action == "2": server_health -= _execute_script_logic(hacker, int(sub_action))
            elif action == "3": _perform_system_reboot(hacker)
            continue

        if player_choice == "1": server_health -= _process_manual_attack(hacker)
        elif player_choice == "2": server_health -= _process_script_menu(hacker)
        elif player_choice == "3": _perform_system_reboot(hacker)
        elif player_choice == "...": console.display_manual()

        if hacker.trace_level >= 100:
            _handle_trace_overload(hacker)
            break

    if server_health <= 0:
        target_server.is_hacked = True
        console.success(f"Acesso USER garantido em {target_server.ip}.")
        return True
    return False

def run_privesc(hacker: Player, target_server: NetworkNode) -> bool:
    """Mini-game para escalada de privilégios (PrivEsc) para ROOT."""
    console.header("PRIVILEGE ESCALATION", "SCANNING FOR KERNEL EXPLOITS")
    console.info("Analisando vulnerabilidades no Kernel do sistema...")
    time.sleep(1.5)

    # O desafio: Encontrar o endereço que termina com '0' (vulnerável)
    addresses = ["0x" + "".join(random.choices("ABCDEF123456789", k=6)) for _ in range(3)]
    vuln_idx = random.randint(0, 2)
    addresses[vuln_idx] = addresses[vuln_idx][:-1] + "0" # Garante que um termina em 0
    
    print("\nDetectamos falhas de memória nestes endereços:")
    for i, addr in enumerate(addresses):
        print(f" [{i}] {addr}")
    
    console.warning("Aponte o ponteiro para o endereço de desvio (terminado em 0):")
    choice = console.ask("Endereço: ")
    
    if choice == str(vuln_idx):
        console.success("\n[SYSTEM] Overflow executado. Permissões elevadas para ROOT.")
        target_server.is_root = True
        return True
    else:
        console.error("\n[SISTEMA] Endereço inválido. O Kernel bloqueou a tentativa!")
        hacker.increase_trace(25)
        return False

def _display_combat_status(hacker, server_health):
    print(f"\n[ALVO]: {server_health} HP | [CONEXÃO]: {hacker.connection_stability}% | [RAM]: {hacker.current_ram}GB")
    console.trace_bar(hacker.trace_level)
    print("\n[1] Ataque Manual | [2] Usar Script | [3] Reboot")

def _process_manual_attack(hacker, auto=False) -> int:
    cmd = random.choice(["bypass --auth", "inject --payload", "flood --packets"])
    console.info(f" >>> DIGITE: {cmd}")
    u_input = cmd if auto else console.ask("> ")
    if u_input == cmd:
        dmg = random.randint(5, 10)
        hacker.increase_trace(2)
        console.success(f"Dano: {dmg}")
        return dmg
    hacker.take_damage(15)
    return 0

def _process_script_menu(hacker: Player) -> int:
    if not hacker.scripts: return 0
    for i, s in enumerate(hacker.scripts): print(f" [{i}] {s.name} ({s.ram_cost}GB)")
    sel = console.ask("Índice (V para voltar): ").upper()
    if sel == 'V': return 0
    try: return _execute_script_logic(hacker, int(sel))
    except: return 0

def _execute_script_logic(hacker: Player, idx: int) -> int:
    s = hacker.scripts[idx]
    if not hacker.use_ram(s.ram_cost): return 0
    if s.id == "phishing": return _run_social_engineering_game(hacker)
    console.system(f"[*] Executando: {s.name}")
    hacker.increase_trace(s.trace_impact)
    return s.damage

def _run_social_engineering_game(hacker: Player) -> int:
    console.header("SOCIAL ENGINEERING", "MANIPULANDO USUÁRIO")
    print("\n[1] Estagiário | [2] Admin Bravo | [3] Manutenção")
    choice = console.ask("Resposta: ")
    if choice == "1":
        console.success("Acesso total garantido.")
        return 100
    hacker.increase_trace(20)
    return 0

def _perform_system_reboot(hacker: Player):
    hacker.restore_system_resources()
    hacker.increase_trace(20)
    console.success("RAM restaurada.")

def _handle_trace_overload(hacker: Player):
    console.error("RASTREIO COMPLETO!")
    hacker.take_damage(100)

def _finalize_hack_session(target_server, server_health) -> bool:
    if server_health <= 0:
        target_server.is_hacked = True
        return True
    return False
