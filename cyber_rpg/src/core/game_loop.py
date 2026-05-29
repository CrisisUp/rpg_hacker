import os
import sys
import time
import random
from entities.player import Player
from systems.generator import generate_network
from systems.combat import start_hack
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
        self.mission_manager = None

    def start(self):
        ui_console.console.clear()
        ui_console.header("INICIALIZANDO TERMINAL DE INVASÃO", "SISTEMA DE PERSISTÊNCIA ATIVO")
        
        if StateManager.save_exists():
            choice = ui_console.ask("Save detectado. Carregar sessão anterior? (S/N): ").upper()
            if choice == 'S':
                save_data = StateManager.load_game()
                self.player = Player(save_data['handle'])
                self.player.from_dict(save_data, get_all_scripts())
                ui_console.success(f"Bem-vindo de volta, {self.player.handle}.")
            else:
                self._new_game()
        else:
            self._new_game()

        self.mission_manager = MissionManager()
        ui_console.system("\n[!] Gerando nova topologia de rede alvo...")
        self.network_root = generate_network(12)
        self.current_node = self.network_root
        self.current_node.is_hacked = True 
        
        ui_console.wait_for_enter("[CONEXÃO ESTABELECIDA] Pressione ENTER para entrar no sistema...")
        self.run_main_loop()

    def _new_game(self):
        player_handle = ui_console.ask("Digite seu Handle (Codename): ")
        self.player = Player(player_handle)
        all_scripts = get_all_scripts()
        if all_scripts:
            # Hacker começa com BruteForce, ProxyHop e agora PHISHING!
            self.player.scripts = [s for s in all_scripts if s.id in ['brute_force', 'proxy_hop', 'phishing']]

    def run_main_loop(self):
        while self.is_running:
            self._display_interface()
            self._check_mission_status()
            
            if not self.is_running: break

            self._display_node_status()
            user_choice = ui_console.ask("Ação: ").upper()
            self._handle_player_action(user_choice)

    def _display_interface(self):
        ui_console.console.clear()
        ui_console.header("SISTEMA DE INVASÃO", "CONEXÃO REMOTA ATIVA")
        ui_console.display_status_table(self.player)
        
        ui_console.console.print(f"\n[bold yellow][MISSÃO]: {self.mission_manager.current_title}[/bold yellow]")
        ui_console.console.print(f"[dim]OBJETIVO: {self.mission_manager.current_description}[/dim]")
        ui_console.trace_bar(self.player.trace_level)
        print("-" * 60)

    def _display_node_status(self):
        print(f"\n[SISTEMA ATUAL]: {self.current_node.ip} ({self.current_node.node_type})")
        if self.current_node.data_files:
            ui_console.info(f"Arquivos: {', '.join(self.current_node.data_files)}")
            print(" [D] Baixar arquivos")
        print("\nConexões detectadas:")
        for index, neighbor in enumerate(self.current_node.connections):
            status = "[bold green]LIBERADO[/]" if neighbor.is_hacked else "[bold red]PROTEGIDO[/]"
            ui_console.console.print(f" [{index}] -> {neighbor.ip} ({neighbor.node_type}) {status}")
        print("\n [Q] Desconectar e Salvar  |  [...] Ajuda")

    def _handle_player_action(self, choice):
        if choice == 'Q':
            StateManager.save_game(self.player.to_dict())
            self.is_running = False
        elif choice == '...':
            ui_console.display_manual()
        elif choice == '....':
            auto_choice = AutoHacker.resolve_navigation(self.player, self.current_node, self.mission_manager)
            self._handle_player_action(auto_choice)
        elif choice == 'D' and self.current_node.data_files:
            self._execute_data_download()
            StateManager.save_game(self.player.to_dict())
        else:
            self._process_navigation(choice)

    def _process_navigation(self, choice):
        try:
            idx = int(choice)
            target = self.current_node.connections[idx]
            if not target.is_hacked:
                if start_hack(self.player, target):
                    self._move_to_node(target)
                else:
                    self._handle_failed_hack()
            else:
                self._move_to_node(target)
        except (ValueError, IndexError):
            pass

    def _move_to_node(self, node):
        self.current_node = node
        self.player.restore_system_resources()
        ui_console.success(f"Salto concluído para {node.ip}")

    def _execute_data_download(self):
        ui_console.system("\n[*] Interceptando pacotes...")
        for file in list(self.current_node.data_files):
            time.sleep(0.5)
            gain = random.randint(100, 300)
            ui_console.success(f"Baixado: {file} (+${gain})")
            self.player.receive_loot(file, gain)
            self.current_node.data_files.remove(file)
        ui_console.wait_for_enter()

    def _check_mission_status(self):
        completed_mission = self.mission_manager.check_objective(self.player.collected_data)
        if completed_mission:
            ui_console.header("MISSÃO CONCLUÍDA", "OBJETIVO ALCANÇADO")
            ui_console.success(f"Arquivo Crítico: {completed_mission['required_file']}")
            self.player.add_credits(completed_mission['reward_credits'])
            StateManager.save_game(self.player.to_dict())
            if self.mission_manager.is_story_complete:
                ui_console.success("\n[SISTEMA] OMNICORP DERRUBADA. VOCÊ VENCEU.")
                self.is_running = False
            ui_console.wait_for_enter()

    def _handle_failed_hack(self):
        if self.player.connection_stability <= 0 or self.player.trace_level >= 100:
            self._trigger_game_over()
        ui_console.wait_for_enter("[FALHA] Conexão instável. ENTER...")

    def _trigger_game_over(self):
        ui_console.console.clear()
        ui_console.error("CONEXÃO PERDIDA - SEU DISCO FOI FORMATADO PELAS AUTORIDADES")
        StateManager.delete_save()
        self.is_running = False
        sys.exit()
