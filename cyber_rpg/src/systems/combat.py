import random
import time
from ui import console
from ui.combat_ui import CombatUI
from entities.player import Player
from entities.network import NetworkNode
from entities.script import HackingScript
from systems.auto_hacker import AutoHacker
from systems.script_effects import get_effect
from core.logger import AuditLogger

class CombatSession:
    """Encapsula o estado e a lógica de um combate de hacking (SRP)."""
    def __init__(self, hacker: Player, target_server: NetworkNode):
        self.hacker = hacker
        self.target_server = target_server
        self.server_health = 0
        
        # Padrão Dispatch para as ações do jogador no combate
        self.actions_map = {
            '1': self._action_manual_attack,
            '2': self._action_script_menu,
            '3': self._action_system_reboot,
            '...': self._action_show_manual,
            '....': self._action_auto_hack
        }

    def execute(self) -> bool:
        CombatUI.display_header(self.target_server.ip)
        self._check_for_rival()
        self._calculate_initial_health()
        
        AuditLogger.log("COMBATE", f"Iniciando tentativa de invasão em {self.target_server.ip} ({self.target_server.node_type})")
        
        while self.server_health > 0 and self.hacker.connection_stability > 0:
            CombatUI.display_status(self.hacker, self.server_health)
            player_choice = CombatUI.ask_action()

            # Despacha a ação e captura o dano retornado (se houver)
            action_func = self.actions_map.get(player_choice)
            if action_func:
                damage = action_func()
                if damage and isinstance(damage, int):
                    self.server_health -= damage
            
            # Contra-medidas após ação do jogador (se não for abrir o manual)
            if self.server_health > 0 and player_choice != "...":
                self._trigger_counter_measures()

            if self.hacker.trace_level >= 100:
                self._handle_trace_overload()
                break

        return self._finalize_hack_session()

    def _check_for_rival(self):
        if self.target_server.rival_present:
            console.error("!!! INTERCEPTAÇÃO: HACKER RIVAL ZERO_COOL DETECTADO !!!")
            console.warning("Ele está tentando bloquear seu acesso e roubar seus pacotes.")
            AuditLogger.log("COMBATE", f"Confronto direto com Zero_Cool em {self.target_server.ip}")
            time.sleep(1.5)

    def _calculate_initial_health(self):
        base_health = 40 if "Firewall" in self.target_server.node_type else 25
        alert_bonus = self.hacker.alert_level * 5
        notoriety_bonus = self.hacker.notoriety * 2
        rival_bonus = 30 if self.target_server.rival_present else 0
        
        self.server_health = base_health + alert_bonus + notoriety_bonus + rival_bonus
        
        if self.hacker.alert_level > 0 or self.hacker.notoriety > 0 or self.target_server.rival_present:
            msg = f"DEFESAS ATIVAS!"
            if self.hacker.alert_level > 0: msg += f" Nível de alerta {self.hacker.alert_level}."
            if self.hacker.notoriety > 0: msg += f" Notoriedade detectada: {self.hacker.notoriety}."
            if self.target_server.rival_present: msg += " [RIVAL PRESENTE]"
            console.warning(f"{msg} (+{alert_bonus + notoriety_bonus + rival_bonus} HP)")

    # --- Ações do Combate (Commands) ---
    def _action_manual_attack(self) -> int:
        return _process_manual_attack(self.hacker)

    def _action_script_menu(self) -> int:
        return _process_script_menu(self.hacker, self.target_server)

    def _action_system_reboot(self):
        _perform_system_reboot(self.hacker)
        return 0

    def _action_show_manual(self):
        console.display_manual()
        return 0

    def _action_auto_hack(self) -> int:
        action, sub_action = AutoHacker.resolve_combat(self.hacker, self.server_health)
        if action == "1":
            return _process_manual_attack(self.hacker, auto=True)
        elif action == "2":
            return _execute_script_logic(self.hacker, int(sub_action), self.target_server)
        elif action == "3":
            _perform_system_reboot(self.hacker)
        return 0
    # ----------------------------------

    def _trigger_counter_measures(self):
        """Chance do servidor reagir com contra-medidas (ICE)."""
        chance = 20 + (self.hacker.trace_level // 5) + (self.hacker.alert_level * 10)
        
        if random.randint(1, 100) <= chance:
            action = random.choice(["REGEN", "TRACE", "STABILITY"])
            
            if action == "REGEN":
                regen = random.randint(5, 10)
                self.server_health += regen
                console.warning(f"ICE DETECTADO: Rotação de criptografia! (+{regen} HP para o servidor)")
                AuditLogger.log("ICE", f"Servidor {self.target_server.ip} recuperou {regen} HP.")
                
            elif action == "TRACE":
                extra_trace = random.randint(10, 20)
                self.hacker.increase_trace(extra_trace)
                console.error(f"ICE DETECTADO: Rastreio Ativo! (+{extra_trace}% Trace)")
                AuditLogger.log("ICE", f"Servidor {self.target_server.ip} forçou rastreio (+{extra_trace}%).")
                
            elif action == "STABILITY":
                dmg = random.randint(10, 20)
                self.hacker.take_damage(dmg)
                console.error(f"ICE DETECTADO: Sobrecarga de pacotes! (-{dmg}% Estabilidade de Conexão)")
                AuditLogger.log("ICE", f"Servidor {self.target_server.ip} atacou estabilidade (-{dmg}%).")
                
            time.sleep(1)

    def _handle_trace_overload(self):
        AuditLogger.log("ALERTA", "Nível de rastreio crítico atingido (100%)!")
        console.error("RASTREIO COMPLETO!"); self.hacker.take_damage(100)

    def _finalize_hack_session(self) -> bool:
        success = self.server_health <= 0
        if success:
            self.target_server.is_hacked = True
            if self.target_server.rival_present:
                console.success("Zero_Cool desconectado! Você recuperou os dados roubados.")
                self.target_server.rival_present = False
                AuditLogger.log("COMBATE", f"Zero_Cool derrotado em {self.target_server.ip}")
            AuditLogger.log("COMBATE", f"Sucesso na invasão de {self.target_server.ip}.")
        else:
            AuditLogger.log("COMBATE", f"Falha na invasão de {self.target_server.ip} (Conexão Perdida/Trace).")
        return success


# Mantemos o wrapper para compatibilidade com o GameLoop
def start_hack(hacker: Player, target_server: NetworkNode) -> bool:
    session = CombatSession(hacker, target_server)
    return session.execute()


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
        console.success("Acesso ROOT garantido."); target_server.is_root = True
        AuditLogger.log("PRIVILEGE_ESC", f"Privilégios ROOT obtidos em {target_server.ip}")
        return True
    
    hacker.increase_trace(25)
    AuditLogger.log("PRIVILEGE_ESC", f"Falha ao escalar privilégios em {target_server.ip}. Trace aumentado.")
    return False

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
        AuditLogger.log("SCRIPT", f"Executando {script.name} em {target_node.ip}")
        return effect.execute(hacker, target_node, script)
    except:
        return 0

def _perform_system_reboot(hacker: Player):
    AuditLogger.log("SISTEMA", "Reinicialização de sistema executada.")
    hacker.restore_system_resources(); hacker.increase_trace(20); console.success("RAM restaurada.")
