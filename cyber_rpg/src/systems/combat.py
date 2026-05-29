import random
import time
from ui import console
from entities.player import Player
from entities.network import NetworkNode
from entities.script import HackingScript
from systems.auto_hacker import AutoHacker

def start_hack(hacker: Player, target_server: NetworkNode) -> bool:
    console.header(f"INICIANDO INVASÃO: {target_server.ip}")
    server_health = 40 if "Firewall" in target_server.node_type else 25
    
    while server_health > 0 and hacker.connection_stability > 0:
        _display_combat_status(hacker, server_health)
        player_choice = console.ask("Ação [1-3] ou '....': ")

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
    console.header("PRIVILEGE ESCALATION", "SCANNING FOR KERNEL EXPLOITS")
    time.sleep(1.5)
    addresses = ["0x" + "".join(random.choices("ABCDEF123456789", k=6)) for _ in range(3)]
    vuln_idx = random.randint(0, 2)
    addresses[vuln_idx] = addresses[vuln_idx][:-1] + "0"
    for i, addr in enumerate(addresses): print(f" [{i}] {addr}")
    choice = console.ask("Endereço (terminado em 0): ")
    if choice == str(vuln_idx):
        console.success("Acesso ROOT garantido."); target_server.is_root = True; return True
    hacker.increase_trace(25); return False

def _display_combat_status(hacker, server_health):
    print(f"\n[ALVO]: {server_health} HP | [CONEXÃO]: {hacker.connection_stability}% | [RAM]: {hacker.current_ram}GB")
    console.trace_bar(hacker.trace_level)
    print("\n[1] Ataque Manual | [2] Usar Script | [3] Reboot")

def _process_manual_attack(hacker, auto=False) -> int:
    cmd = random.choice(["bypass --auth", "inject --payload", "flood --packets"])
    console.info(f" >>> DIGITE RÁPIDO: {cmd}")
    u_input = cmd if auto else console.ask("> ")
    if u_input == cmd:
        dmg = random.randint(5, 10); hacker.increase_trace(2); console.success(f"Dano: {dmg}"); return dmg
    hacker.take_damage(15); return 0

def _process_script_menu(hacker, target_node) -> int:
    if not hacker.scripts: return 0
    for i, s in enumerate(hacker.scripts): print(f" [{i}] {s.name} ({s.ram_cost}GB)")
    sel = console.ask("Índice (V para voltar): ").upper()
    if sel == 'V': return 0
    try: return _execute_script_logic(hacker, int(sel), target_node)
    except: return 0

def _execute_script_logic(hacker, idx: int, target_node) -> int:
    s = hacker.scripts[idx]
    
    if s.id == "zeroday":
        console.header("ZERO-DAY EXPLOIT ATIVADO", "EXECUTANDO VULNERABILIDADE DESCONHECIDA")
        hacker.remove_script("zeroday")
        return 999

    if not hacker.use_ram(s.ram_cost): console.error("RAM insuficiente!"); return 0
    
    if s.id == "phishing": return _run_social_engineering_game(hacker)
    if s.id == "xss":
        if "Web Server" in target_node.node_type:
            console.success("Payload XSS injetado."); target_node.is_xss_active = True; return 100
        console.error("Apenas para Web Servers!"); return 0

    if s.id == "overflow":
        console.warning("!!! EXECUTANDO OVERFLOW !!!")
        target_node.is_corrupted = True; target_node.data_files = []
        hacker.increase_trace(s.trace_impact); return 100

    if s.id == "decrypter":
        if target_node.is_under_ransomware:
            console.success("Ransomware neutralizado!"); target_node.ransomware_timer = 0; return 0
        console.error("Servidor não infectado."); return 0

    if s.id == "supplychain":
        if "Supplier" in target_node.node_type or "Partner" in target_node.node_type:
            console.success("Backdoor plantado na atualização de software do fornecedor.")
            target_node.is_supply_chain_infected = True; target_node.backdoor_timer = 4
            return 100 
        console.error("Este script só funciona em alvos externos (Supplier/Partner)!"); return 0

    console.system(f"[*] Executando: {s.name}")
    hacker.increase_trace(s.trace_impact)
    return s.damage

def _run_social_engineering_game(hacker: Player) -> int:
    scenarios = [
        {
            "persona": "Estagiário de TI (Nervoso)",
            "context": "O estagiário atendeu o chat de suporte interno.",
            "prompt": "Oi! Desculpa a demora. Eu não consigo achar o ticket de manutenção do seu servidor. Qual era o código mesmo?",
            "options": [
                {"text": "Diga que é urgente: 'Código 404-X. Se eu não logar agora, o CEO vai me matar!'", "success": True, "trace": 5},
                {"text": "Seja técnico: 'A porta 8080 está em loop infinito, preciso de acesso root para o kill -9.'", "success": False, "trace": 30},
                {"text": "Ameace: 'Você é novo? Me passa o acesso ou ligo pro seu supervisor agora!'", "success": True, "trace": 50}
            ]
        },
        {
            "persona": "Analista de RH (Ocupada)",
            "context": "Você enviou um e-mail falso sobre 'Bônus de Performance'.",
            "prompt": "Recebi seu e-mail, mas o link está pedindo minha credencial de admin. É seguro?",
            "options": [
                {"text": "Minta com calma: 'Sim, é a nova política de segurança Zero-Trust da empresa.'", "success": True, "trace": 10},
                {"text": "Pressione: 'O prazo para o bônus acaba em 5 minutos. Você quem sabe.'", "success": True, "trace": 40},
                {"text": "Ignore e envie outro link: 'Tente este portal alternativo de contingência.'", "success": False, "trace": 60}
            ]
        },
        {
            "persona": "Segurança de Plantão (Cético)",
            "context": "Você ligou simulando ser da manutenção predial.",
            "prompt": "Estranho... não recebi nenhum aviso de manutenção no andar 4 hoje.",
            "options": [
                {"text": "Use jargão de infra: 'Houve um vazamento no chiller principal. Se não isolarmos a sala de racks, vai fritar tudo.'", "success": True, "trace": 20},
                {"text": "Fingir erro: 'Ah, desculpe, deve ser no andar 5 então. Pode conferir pra mim?'", "success": False, "trace": 15},
                {"text": "Confusão burocrática: 'Verifique a Ordem de Serviço #8829-B no sistema legado.'", "success": True, "trace": 5}
            ]
        }
    ]

    scenario = random.choice(scenarios)
    console.header("SOCIAL ENGINEERING", scenario["persona"])
    console.info(scenario["context"])
    print(f"\n[FALA]: \"{scenario['prompt']}\"")
    
    for i, opt in enumerate(scenario["options"]):
        print(f" [{i}] {opt['text']}")
    
    choice = console.ask("Sua escolha: ")
    try:
        opt = scenario["options"][int(choice)]
        if opt["success"]:
            console.success("O alvo caiu na armadilha! Acesso garantido.")
            hacker.increase_trace(opt["trace"])
            return 100
        else:
            console.error("O alvo desconfiou e bloqueou a tentativa.")
            hacker.increase_trace(opt["trace"])
            hacker.take_damage(20)
            return 0
    except:
        console.warning("Hesitação detectada. O alvo encerrou o chat.")
        hacker.increase_trace(10)
        return 0

def _perform_system_reboot(hacker: Player):
    hacker.restore_system_resources(); hacker.increase_trace(20); console.success("RAM restaurada.")

def _handle_trace_overload(hacker: Player):
    console.error("RASTREIO COMPLETO!"); hacker.take_damage(100)

def _finalize_hack_session(target_server, server_health) -> bool:
    if server_health <= 0: target_server.is_hacked = True; return True
    return False
