import random
import time
from ui import console
from ui.combat_ui import CombatUI
from entities.player import Player
from entities.network import NetworkNode
from entities.script import HackingScript
from systems.auto_hacker import AutoHacker
from systems.script_effects import get_effect

def start_hack(hacker: Player, target_server: NetworkNode) -> bool:
    CombatUI.display_header(target_server.ip)
    server_health = 40 if "Firewall" in target_server.node_type else 25
    
    while server_health > 0 and hacker.connection_stability > 0:
        CombatUI.display_status(hacker, server_health)
        player_choice = CombatUI.ask_action()

        if player_choice == "....":
            action, sub_action = AutoHacker.resolve_combat(hacker, server_health)
            if action == "1": server_health -= _process_manual_attack(hacker, auto=True)
            elif action == "2": server_health -= _execute_script_logic(hacker, int(sub_action), target_server)
            elif action == "3": _perform_system_reboot(hacker)
            continue

        if player_choice == "1": server_health -= _process_manual_attack(hacker)
        elif player_choice == "2": server_health -= _process_script_menu(hacker, target_server)
        elif player_choice == "3": _perform_system_reboot(hacker)
        elif player_choice == "...": console.display_manual()

        if hacker.trace_level >= 100:
            _handle_trace_overload(hacker)
            break

    return _finalize_hack_session(target_server, server_health)

def run_privesc(hacker: Player, target_server: NetworkNode) -> bool:
    if target_server.is_corrupted:
        console.error("Sistemas de autenticação destruídos.")
        return False
    
    time.sleep(1.5)
    addresses = ["0x" + "".join(random.choices("ABCDEF123456789", k=6)) for _ in range(3)]
    vuln_idx = random.randint(0, 2)
    addresses[vuln_idx] = addresses[vuln_idx][:-1] + "0"
    
    choice = CombatUI.display_privesc_challenge(addresses)
    if choice == str(vuln_idx):
        console.success("Acesso ROOT garantido."); target_server.is_root = True; return True
    hacker.increase_trace(25); return False

def _process_manual_attack(hacker, auto=False) -> int:
    cmd = random.choice(["bypass --auth", "inject --payload", "flood --packets"])
    u_input = cmd if auto else CombatUI.ask_manual_cmd(cmd)
    if u_input == cmd:
        dmg = random.randint(5, 10); hacker.increase_trace(2); console.success(f"Dano: {dmg}"); return dmg
    hacker.take_damage(15); return 0

def _process_script_menu(hacker, target_node) -> int:
    if not hacker.scripts: return 0
    sel = CombatUI.display_script_menu(hacker.scripts)
    if sel == 'V': return 0
    try: return _execute_script_logic(hacker, int(sel), target_node)
    except: return 0

def _execute_script_logic(hacker, idx: int, target_node) -> int:
    try:
        script = hacker.scripts[idx]
        if script.id != "zeroday" and not hacker.use_ram(script.ram_cost):
            console.error("RAM insuficiente!")
            return 0
        effect = get_effect(script.id)
        return effect.execute(hacker, target_node, script)
    except:
        return 0

def _perform_system_reboot(hacker: Player):
    hacker.restore_system_resources(); hacker.increase_trace(20); console.success("RAM restaurada.")

def _handle_trace_overload(hacker: Player):
    console.error("RASTREIO COMPLETO!"); hacker.take_damage(100)

def _finalize_hack_session(target_server, server_health) -> bool:
    if server_health <= 0: target_server.is_hacked = True; return True
    return False
