import os, sys, time, random
from entities.player import Player
from entities.network import NetworkNode
from systems.generator import generate_network
from systems.combat import start_hack, run_privesc
from ui import console as ui_console
from systems.loader import get_all_scripts
from systems.missions import MissionManager
from systems.auto_hacker import AutoHacker
from core.state import StateManager

class GameLoop:
    def __init__(self):
        self.is_running = True
        self.player = None
        self.current_node = None
        self.network_root = None
        self.all_network_nodes = []
        self.mission_manager = None

    def start(self):
        ui_console.console.clear()
        ui_console.header("INICIALIZANDO TERMINAL DE INVASÃO")
        if StateManager.save_exists():
            choice = ui_console.ask("Save detectado. Carregar? (S/N): ").upper()
            if choice == 'S':
                save_data = StateManager.load_game()
                self.player = Player(save_data['handle'])
                self.player.from_dict(save_data, get_all_scripts())
            else: self._new_game()
        else: self._new_game()
        self.mission_manager = MissionManager()
        self.network_root = generate_network(15)
        self._collect_all_nodes(self.network_root)
        self.current_node = self.network_root
        self.current_node.is_hacked = True; self.current_node.is_root = True 
        self.run_main_loop()

    def _collect_all_nodes(self, root):
        stack, visited = [root], set()
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node); self.all_network_nodes.append(node)
                stack.extend(node.connections)

    def _new_game(self):
        handle = ui_console.ask("Handle: ")
        self.player = Player(handle)
        all_s = get_all_scripts()
        if all_s: self.player.scripts = [s for s in all_s if s.id in ['brute_force', 'proxy_hop', 'mitm', 'phishing', 'xss']]

    def run_main_loop(self):
        while self.is_running:
            self._display_interface()
            self._process_passive_actions()
            self._check_mission_status()
            if not self.is_running: break
            self._display_node_status()
            choice = ui_console.ask("Ação: ").upper()
            self._handle_player_action(choice)

    def _process_passive_actions(self):
        """Processa MITM e XSS em segundo plano."""
        # 1. Processar MITM
        sniffers = [n for n in self.all_network_nodes if n.is_sniffing]
        for node in sniffers:
            if random.random() < 0.20:
                gain = random.randint(50, 150); self.player.add_credits(gain)
                ui_console.success(f"MITM {node.ip}: +${gain}")
            self.player.increase_trace(1)

        # 2. Processar XSS (Fisgar Workstations)
        infected_sites = [n for n in self.all_network_nodes if n.is_xss_active]
        for node in infected_sites:
            if random.random() < 0.15: # 15% de chance de um funcionário conectar
                new_ip = f"172.16.0.{random.randint(100, 254)}"
                workstation = NetworkNode(new_ip, "Employee Workstation")
                workstation.data_files = ["personal_secrets.txt", "browser_cookies.db"]
                node.connect(workstation)
                self.all_network_nodes.append(workstation)
                ui_console.warning(f"\n[XSS] Alvo fisgado em {node.ip}! Nova workstation detectada: {workstation.ip}")

    def _display_interface(self):
        ui_console.console.clear()
        ui_console.header("SISTEMA DE INVASÃO", "AGENTE GHOST ONLINE")
        ui_console.display_status_table(self.player)
        ui_console.console.print(f"\n[bold yellow][MISSÃO]: {self.mission_manager.current_title}[/bold yellow]")
        ui_console.trace_bar(self.player.trace_level)
        print("-" * 60)

    def _display_node_status(self):
        p_status = "ROOT" if self.current_node.is_root else "USER"
        flags = []
        if self.current_node.is_sniffing: flags.append("Grampeado")
        if self.current_node.is_xss_active: flags.append("Infectado (XSS)")
        status_line = f" [{', '.join(flags)}]" if flags else ""
        print(f"\n[NO ATUAL]: {self.current_node.ip} ({self.current_node.node_type}) - {p_status}{status_line}")
        
        if self.current_node.is_root and not self.current_node.is_sniffing:
            print(" [M] Instalar MITM Sniffer")

        if self.current_node.data_files:
            if self.current_node.is_root:
                ui_console.info(f"Arquivos: {', '.join(self.current_node.data_files)}")
                print(" [D] Baixar arquivos")
            else: print(" [P] Escalar Privilégios (PrivEsc)")

        print("\nConexões detectadas:")
        for i, n in enumerate(self.current_node.connections):
            status = "[ROOT]" if n.is_root else "[USER]" if n.is_hacked else "[LOCKED]"
            ui_console.console.print(f" [{i}] -> {n.ip} ({n.node_type}) {status}")
        print("\n [Q] Sair | [...] Ajuda")

    def _handle_player_action(self, choice):
        if choice == 'Q': StateManager.save_game(self.player.to_dict()); self.is_running = False
        elif choice == '...': ui_console.display_manual()
        elif choice == '....': self._handle_player_action(AutoHacker.resolve_navigation(self.player, self.current_node, self.mission_manager))
        elif choice == 'M' and self.current_node.is_root and not self.current_node.is_sniffing: self._deploy_mitm()
        elif choice == 'D' and self.current_node.data_files and self.current_node.is_root: self._execute_data_download()
        elif choice == 'P' and self.current_node.is_hacked and not self.current_node.is_root:
            if run_privesc(self.player, self.current_node): ui_console.wait_for_enter()
        else: self._process_navigation(choice)

    def _deploy_mitm(self):
        mitm_s = next((s for s in self.player.scripts if s.id == "mitm"), None)
        if self.player.use_ram(mitm_s.ram_cost):
            self.current_node.is_sniffing = True; self.player.increase_trace(mitm_s.trace_impact)
            ui_console.success("Sniffer instalado."); ui_console.wait_for_enter()

    def _process_navigation(self, choice):
        try:
            target = self.current_node.connections[int(choice)]
            if not target.is_hacked:
                if start_hack(self.player, target): self.current_node = target; self.player.restore_system_resources()
            else: self.current_node = target; self.player.restore_system_resources()
        except: pass

    def _execute_data_download(self):
        for file in list(self.current_node.data_files):
            if file == "ZeroDay_Exploit.zip": self._unlock_zeroday()
            else:
                gain = random.randint(100, 300); ui_console.success(f"Baixado: {file} (+${gain})")
                self.player.receive_loot(file, gain)
            self.current_node.data_files.remove(file)
        ui_console.wait_for_enter()

    def _unlock_zeroday(self):
        ui_console.header("LOOT LENDÁRIO", "ZERO-DAY")
        zeroday = next((s for s in get_all_scripts() if s.id == "zeroday"), None)
        if zeroday: self.player.add_script(zeroday); ui_console.success("Instalado.")

    def _check_mission_status(self):
        m = self.mission_manager.check_objective(self.player.collected_data)
        if m:
            ui_console.header("MISSÃO CONCLUÍDA", "OBJETIVO ALCANÇADO")
            self.player.add_credits(m['reward_credits'])
            if self.mission_manager.is_story_complete: ui_console.success("\nVOCÊ VENCEU."); self.is_running = False
            ui_console.wait_for_enter()

    def _trigger_game_over(self):
        ui_console.console.clear(); ui_console.error("DESCONECTADO"); StateManager.delete_save(); self.is_running = False; sys.exit()
