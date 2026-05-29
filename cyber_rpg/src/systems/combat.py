import random
import time
from ui import console
from entities.player import Player
from entities.network import NetworkNode
from entities.script import HackingScript
from systems.auto_hacker import AutoHacker

def start_hack(hacker: Player, target_server: NetworkNode) -> bool:
    """Orquestra a invasão usando força bruta ou engenharia social."""
    console.header(f"INICIANDO INVASÃO: {target_server.ip}")
    
    server_health = 40 if "Firewall" in target_server.node_type else 25
    
    while server_health > 0 and hacker.connection_stability > 0:
        _display_combat_status(hacker, server_health)
        player_choice = console.ask("Ação [1-3] ou '....': ")

        if player_choice == "....":
            action, sub_action = AutoHacker.resolve_combat(hacker, server_health)
            if action == "1":
                server_health -= _process_manual_attack(hacker, auto=True)
            elif action == "2":
                server_health -= _execute_script_logic(hacker, int(sub_action))
            elif action == "3":
                _perform_system_reboot(hacker)
            continue

        if player_choice == "1":
            server_health -= _process_manual_attack(hacker)
        elif player_choice == "2":
            server_health -= _process_script_menu(hacker)
        elif player_choice == "3":
            _perform_system_reboot(hacker)
        elif player_choice == "...":
            console.display_manual()

        if hacker.trace_level >= 100:
            _handle_trace_overload(hacker)
            break

    return _finalize_hack_session(target_server, server_health)

def _display_combat_status(hacker, server_health):
    print(f"\n[ALVO]: {server_health} HP | [CONEXÃO]: {hacker.connection_stability}% | [RAM]: {hacker.current_ram}GB")
    console.trace_bar(hacker.trace_level)
    print("\n[1] Ataque Manual | [2] Usar Script | [3] Reboot")

def _process_manual_attack(hacker: Player, auto=False) -> int:
    commands = ["bypass --auth", "inject --payload", "flood --packets"]
    required_command = random.choice(commands)
    console.info(f" >>> DIGITE RÁPIDO: {required_command}")
    
    if auto:
        time.sleep(1)
        console.system(f"Ghost digitando: {required_command}")
        user_input = required_command
        time_taken = 1
    else:
        start_time = time.time()
        user_input = console.ask("> ")
        time_taken = time.time() - start_time
    
    if user_input == required_command and time_taken <= 7:
        damage = random.randint(5, 10)
        hacker.increase_trace(2)
        console.success(f"Dano: {damage}")
        return damage
    else:
        hacker.take_damage(15)
        console.error("Falha na sincronização!")
        return 0

def _process_script_menu(hacker: Player) -> int:
    if not hacker.scripts:
        console.warning("Arsenal vazio!")
        return 0
    for index, script in enumerate(hacker.scripts):
        print(f" [{index}] {script.name} ({script.ram_cost}GB)")
    selection = console.ask("Índice (V para voltar): ").upper()
    if selection == 'V': return 0
    try:
        return _execute_script_logic(hacker, int(selection))
    except (ValueError, IndexError):
        console.error("Seleção inválida.")
    return 0

def _execute_script_logic(hacker: Player, script_index: int) -> int:
    """Executa a lógica do script, diferenciando entre ataque técnico e social."""
    script = hacker.scripts[script_index]
    
    if not hacker.use_ram(script.ram_cost):
        console.error("RAM insuficiente!")
        return 0

    # Lógica Especial para Engenharia Social (Phishing)
    if script.id == "phishing":
        return _run_social_engineering_game(hacker)

    # Lógica para scripts de ataque técnico comum
    console.system(f"[*] Executando: {script.name}")
    time.sleep(1)
    hacker.increase_trace(script.trace_impact)
    console.success(script.description)
    return script.damage

def _run_social_engineering_game(hacker: Player) -> int:
    """Mini-game de diálogo para Phishing."""
    console.header("SOCIAL ENGINEERING OVERRIDE", "MANIPULANDO USUÁRIO")
    console.info("Um funcionário atendeu seu e-mail falso. Ele está desconfiado.")
    console.system("\nFUNCIONÁRIO: 'Quem é você? Não reconheço seu endereço de TI.'")
    
    print("\nEscolha sua resposta:")
    print(" [1] 'Sou o novo estagiário da rede, desculpe o erro no domínio.'")
    print(" [2] 'Cale a boca! Eu sou o Admin da OmniCorp, obedeça ou será demitido!'")
    print(" [3] 'Estamos em uma manutenção de emergência. Preciso que clique no link agora.'")
    
    choice = console.ask("Sua Mentira: ")
    
    if choice == "1":
        console.success("\nFUNCIONÁRIO: 'Ah, entendi. O pessoal de TI sempre troca os e-mails. Vou clicar.'")
        console.system("[*] O usuário instalou seu backdoor. Acesso total garantido.")
        return 100 # Derruba o servidor na hora
    elif choice == "2":
        console.error("\nFUNCIONÁRIO: 'Nosso Admin está de férias! Você é um impostor!'")
        hacker.increase_trace(40)
        return 0
    else:
        console.warning("\nFUNCIONÁRIO: 'Manutenção agora? Vou ligar para o meu chefe para confirmar...'")
        hacker.increase_trace(15)
        return 5 # Dano mínimo, o golpe não colou bem

def _perform_system_reboot(hacker: Player):
    console.warning("Reiniciando sistema...")
    time.sleep(2)
    hacker.restore_system_resources()
    hacker.increase_trace(20)
    console.success("RAM restaurada.")

def _handle_trace_overload(hacker: Player):
    console.error("RASTREIO COMPLETO!")
    hacker.take_damage(100)

def _finalize_hack_session(target_server, server_health) -> bool:
    if server_health <= 0:
        target_server.is_hacked = True
        console.success(f"Servidor {target_server.ip} comprometido.")
        return True
    return False
