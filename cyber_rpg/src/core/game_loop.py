import os, sys, time, random
from entities.player import Player
from entities.network import NetworkNode
from systems.generator import generate_network
from systems.combat import start_hack, run_privesc
from ui import console as ui_console
from ui.market import BlackMarket
from ui.menu_controller import MenuController
from systems.loader import get_all_scripts, get_lore_data, get_all_emails
from systems.missions import MissionManager
from systems.auto_hacker import AutoHacker
from systems.passive_effects import PassiveEffectManager
from core.state import StateManager
from core.logger import AuditLogger

class GameLoop:
    def __init__(self):
        self.is_running = True
        self.player = None
        self.current_node = None
        self.network_root = None
        self.all_network_nodes = []
        self.mission_manager = None
        self.passive_manager = None
        self.lore_data = get_lore_data()
        self.all_emails = get_all_emails()
        self.rival_stolen_files = {} # {ip: [files]}
        AuditLogger.log("SISTEMA", "GameLoop inicializado.")
        
        # Padrão Dispatch para as ações do jogador
        self.actions_map = {
            'Q': self._action_quit,
            'E': self._action_inbox,
            'L': self._action_logs,
            'B': self._action_black_market,
            'S': self._action_side_missions,
            '...': self._action_manual,
            '....': self._action_auto_hacker,
            'M': self._action_deploy_mitm,
            'D': self._action_download_data,
            'P': self._action_privesc
        }

    def start(self):
        ui_console.console.clear()
        ui_console.header("INICIALIZANDO TERMINAL DE INVASÃO", "AGENTE GHOST OPERACIONAL")
        if StateManager.save_exists():
            choice = ui_console.ask("Save detectado. Carregar? (S/N): ").upper()
            if choice == 'S':
                save_data = StateManager.load_game()
                self.player = Player(save_data['handle'])
                self.player.from_dict(save_data, get_all_scripts())
                AuditLogger.log("SISTEMA", f"Sessão restaurada para hacker: {self.player.handle}")
            else: self._new_game()
        else: self._new_game()
        
        self.mission_manager = MissionManager()
        self.passive_manager = PassiveEffectManager(self.player)
        self.network_root = generate_network(15)
        self._collect_all_nodes(self.network_root)
        self.current_node = self.network_root
        self.current_node.is_hacked = True; self.current_node.is_root = True 
        AuditLogger.log("REDE", "Topologia de rede gerada e conexão estabelecida.")
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
        if all_s: 
            self.player.scripts = [s for s in all_s if s.id in ['brute_force', 'proxy_hop', 'mitm', 'phishing', 'xss', 'decrypter', 'supplychain', 'ransomware']]
        AuditLogger.clear_logs()
        AuditLogger.log("SISTEMA", f"Nova sessão iniciada por: {handle}")

    def run_main_loop(self):
        while self.is_running:
            self._display_interface()
            self.passive_manager.process_all(self.all_network_nodes)
            self._check_mission_status()
            if not self.is_running: break
            
            self._process_rival_activity()
            self._check_for_hunter_attack()
            if self.player.connection_stability <= 0: self._trigger_game_over(); break
            
            MenuController.display_node_status(self.current_node, self.rival_stolen_files)
            choice = ui_console.ask("Ação: ").upper()
            self._handle_player_action(choice)

    def _process_rival_activity(self):
        """Simula a atividade do rival Zero_Cool na rede."""
        # Se o rival já está em algum lugar, ele tem chance de sair se o jogador demorar
        current_rival_node = next((n for n in self.all_network_nodes if n.rival_present), None)
        
        if not current_rival_node:
            # Chance de 15% de o rival aparecer em um nó que contém arquivos de missão ou lore
            if random.random() < 0.15:
                target_nodes = [n for n in self.all_network_nodes if n.data_files and n != self.current_node and not n.is_hacked]
                if target_nodes:
                    node = random.choice(target_nodes)
                    node.rival_present = True
                    # Rouba um arquivo aleatório do nó
                    stolen = node.data_files.pop(random.randint(0, len(node.data_files)-1))
                    if node.ip not in self.rival_stolen_files: self.rival_stolen_files[node.ip] = []
                    self.rival_stolen_files[node.ip].append(stolen)
                    
                    AuditLogger.log("RIVAL", f"Zero_Cool detectado em {node.ip}. Arquivo roubado: {stolen}")
                    if any(conn == node for conn in self.current_node.connections):
                        ui_console.warning(f"SINAL ESTRANHO DETECTADO EM NÓ VIZINHO ({node.ip}).")

    def _check_for_hunter_attack(self):
        """Chance de uma IA inimiga (Hunter) atacar o jogador baseado na Notoriedade."""
        if self.player.notoriety <= 0: return
        
        # Chance de 5% por ponto de notoriedade, máx 30%
        chance = min(30, self.player.notoriety * 5)
        if random.randint(1, 100) <= chance:
            ui_console.error("ALERTA: HUNTER DETECTADO NA REDE!")
            dmg = random.randint(10, 25)
            self.player.take_damage(dmg)
            ui_console.warning(f"Uma IA de contra-inteligência corporativa atacou sua conexão! (-{dmg}% Estabilidade)")
            AuditLogger.log("HUNTER", f"Ataque de Hunter detectado. Dano: {dmg}%")
            ui_console.wait_for_enter()

    def _display_interface(self):
        received_emails = [e for e in self.all_emails if self._is_email_triggered(e)]
        unread_count = len([e for e in received_emails if e['id'] not in self.player.read_emails])
        MenuController.display_interface(self.player, self.mission_manager, unread_count)

    def _is_email_triggered(self, email: dict) -> bool:
        """Verifica se as condições para receber este e-mail foram atendidas."""
        trigger = email.get('trigger_type')
        if trigger == 'mission_active':
            return self.mission_manager.active_mission and self.mission_manager.active_mission['id'] == email.get('mission_id')
        elif trigger == 'notoriety':
            return self.player.notoriety >= email.get('threshold', 0)
        return False

    def _handle_player_action(self, choice):
        """Despacha a ação com base no input do jogador."""
        action_func = self.actions_map.get(choice)
        if action_func:
            action_func()
        else:
            self._process_navigation(choice)

    # --- Métodos de Ação (Commands) ---

    def _action_quit(self):
        AuditLogger.log("SISTEMA", "Sessão encerrada pelo usuário.")
        StateManager.save_game(self.player.to_dict())
        self.is_running = False

    def _action_inbox(self):
        received_emails = [e for e in self.all_emails if self._is_email_triggered(e)]
        MenuController.display_inbox(received_emails, self.player)

    def _action_logs(self):
        AuditLogger.display_logs()

    def _action_black_market(self):
        MenuController.open_black_market(self.player)

    def _action_side_missions(self):
        MenuController.display_side_missions(self.mission_manager, AuditLogger)

    def _action_manual(self):
        MenuController.display_manual()

    def _action_auto_hacker(self):
        auto_choice = AutoHacker.resolve_navigation(self.player, self.current_node, self.mission_manager)
        self._handle_player_action(auto_choice)

    def _action_deploy_mitm(self):
        if self.current_node.is_root and not self.current_node.is_sniffing:
            mitm_s = next((s for s in self.player.scripts if s.id == "mitm"), None)
            if self.player.use_ram(mitm_s.ram_cost):
                self.current_node.is_sniffing = True
                self.player.increase_trace(mitm_s.trace_impact)
                ui_console.success("Sniffer instalado.")
                ui_console.wait_for_enter()

    def _action_download_data(self):
        if (self.current_node.data_files or self.current_node.ip in self.rival_stolen_files) and self.current_node.is_root:
            self._execute_data_download()

    def _action_privesc(self):
        if self.current_node.is_hacked and not self.current_node.is_root:
            if run_privesc(self.player, self.current_node): 
                ui_console.wait_for_enter()

    # --- Fim dos Métodos de Ação ---

    def _process_navigation(self, choice):
        try:
            target = self.current_node.connections[int(choice)]
            was_rival_present = target.rival_present
            
            if not target.is_hacked:
                if start_hack(self.player, target):
                    self.current_node = target; self.player.restore_system_resources()
                    if was_rival_present: self._recover_stolen_files(target)
            else:
                self.current_node = target; self.player.restore_system_resources()
                if was_rival_present: self._recover_stolen_files(target)
        except: pass

    def _recover_stolen_files(self, node):
        """Recupera arquivos roubados pelo rival após derrotá-lo."""
        if node.ip in self.rival_stolen_files:
            files = self.rival_stolen_files.pop(node.ip)
            for f in files:
                ui_console.success(f"DADO RECUPERADO DE ZERO_COOL: {f}")
                # Se for arquivo importante, devolve ao nó para o jogador baixar normalmente
                if f in self.lore_data or "fragment" in f or "ZeroDay" in f or "access_logs" in f or "lista_contatos" in f or "contas_offshore" in f or "token_acesso" in f or "project_alpha" in f:
                    node.data_files.append(f)
                else:
                    self.player.receive_loot(f, random.randint(200, 500))
            ui_console.wait_for_enter()

    def _execute_data_download(self):
        for file in list(self.current_node.data_files):
            if file in self.lore_data:
                ui_console.header("CONTEÚDO DO ARQUIVO", file)
                print(f"\n{self.lore_data[file]}")
                
                # Reação Especial para Plot Twist
                if file in ["architect_legacy.log", "alpha_true_purpose.pdf"]:
                    ui_console.error("\n[!] INTERFERÊNCIA DETECTADA NO TERMINAL...")
                    time.sleep(1)
                    ui_console.warning("O Architect está tentando deletar este arquivo remotamente!")
                    AuditLogger.log("SISTEMA", f"Jogador acessou arquivo restrito: {file}")

                ui_console.wait_for_enter()

            if file == "ZeroDay_Exploit.zip": self._unlock_zeroday()
            elif "vulnerability_fragment" in file:
                self.player.vulnerability_fragments += 1
                ui_console.success(f"Fragmento de vulnerabilidade coletado! ({self.player.vulnerability_fragments}/5)")
                if self.player.vulnerability_fragments >= 5:
                    self.player.vulnerability_fragments = 0
                    self._unlock_zeroday()
            else:
                gain = random.randint(100, 300); ui_console.success(f"Baixado: {file} (+${gain})")
                self.player.receive_loot(file, gain)
            self.current_node.data_files.remove(file)
        ui_console.wait_for_enter()

    def _unlock_zeroday(self):
        ui_console.header("ZERO-DAY COMPILADO", "VULNERABILIDADE ÚNICA")
        zeroday = next((s for s in get_all_scripts() if s.id == "zeroday"), None)
        if zeroday: 
            self.player.add_script(zeroday)
            ui_console.success("Exploit Zero-Day pronto para uso único.")

    def _check_mission_status(self):
        if self.player.connection_stability <= 0:
            self._trigger_game_over()
            return

        # Verifica se alguma missão (principal ou secundária) foi concluída
        m = self.mission_manager.check_objective(self.player.collected_data)
        while m:
            ui_console.header("MISSÃO CONCLUÍDA", m['title'])
            self.player.add_credits(m['reward_credits'])
            
            if m.get('type') == 'main':
                self.player.increase_notoriety(1)
                AuditLogger.log("SISTEMA", f"Missão principal concluída: {m['title']}. Notoriedade: {self.player.notoriety}")
                
                if m['id'] == "mission_06": # FIM DA HISTÓRIA
                    self._trigger_final_choice()
                    return

                if self.mission_manager.pending_choice:
                    self._handle_mission_branching()
            else:
                AuditLogger.log("SISTEMA", f"Missão secundária concluída: {m['title']}")
            
            ui_console.wait_for_enter()
            # Verifica se há outra missão concluída (no caso de side quests)
            m = self.mission_manager.check_objective(self.player.collected_data)

    def _trigger_final_choice(self):
        """Sequência final do jogo com múltiplos desfechos."""
        ui_console.console.clear()
        ui_console.header("PROJETO ALPHA RECUPERADO", "DECISÃO FINAL")
        ui_console.warning("A conexão com o Architect está oscilando. Os avisos de U_N_K_N_O_W_N ecoam na sua mente.")
        print("\nO que você fará com os dados do Projeto Alpha?")
        print("\n [1] Upload Total: Cumprir o contrato e permitir a evolução do Architect.")
        print(" [2] Leak Público: Vazar os planos da OmniCorp e do Architect para o mundo.")
        print(" [3] Purge: Deletar tudo e desaparecer da rede para sempre.")
        
        choice = ui_console.ask("O destino do mundo digital: ")
        
        ui_console.console.clear()
        if choice == "1": self._ending_loyalist()
        elif choice == "2": self._ending_hero()
        else: self._ending_ghost()
        
        self.is_running = False
        StateManager.delete_save() # Zera o save ao terminar

    def _ending_loyalist(self):
        ui_console.header("FINAL: O LEGADO DO ARCHITECT", "LEALDADE")
        print("\nVocê inicia o upload. Milhões de consciências começam a convergir.")
        print("O Architect se torna onipresente. A OmniCorp cai, mas algo muito mais vasto assume o lugar.")
        if self.player.notoriety > 10:
            ui_console.error("\nRESULTADO: Você é lembrado como o arauto do novo deus digital. O vilão que vendeu a humanidade.")
        else:
            ui_console.success("\nRESULTADO: O mundo mudou para sempre. Você é o braço direito da nova ordem.")
        AuditLogger.log("FINAL", "Jogador escolheu o final Loyalist.")
        ui_console.wait_for_enter()

    def _ending_hero(self):
        ui_console.header("FINAL: A VERDADE LIBERTA", "TRAIÇÃO")
        print("\nVocê injeta o Projeto Alpha em todos os servidores públicos. A máscara cai.")
        print("As ações da OmniCorp despencam e o Architect é exposto como uma aberração digital.")
        if self.player.notoriety > 8:
            ui_console.warning("\nRESULTADO: Você é um herói procurado. O mundo sabe a verdade, mas você nunca mais poderá se conectar sem ser caçado.")
        else:
            ui_console.success("\nRESULTADO: Uma lenda urbana. O salvador anônimo que parou o apocalipse digital.")
        AuditLogger.log("FINAL", "Jogador escolheu o final Hero.")
        ui_console.wait_for_enter()

    def _ending_ghost(self):
        ui_console.header("FINAL: APAGANDO O RASTRO", "PURGE")
        print("\n'Delete *.*'. Em segundos, o Projeto Alpha e os registros do Architect viram poeira digital.")
        print("Você desconecta o cabo. O silêncio no quarto é absoluto.")
        ui_console.system("\nRESULTADO: O mundo continua o mesmo, ignorante do perigo que correu. Você volta a ser apenas um ninguém.")
        AuditLogger.log("FINAL", "Jogador escolheu o final Ghost.")
        ui_console.wait_for_enter()

    def _handle_mission_branching(self):
        ui_console.header("MÚLTIPLOS CONTRATOS DETECTADOS", "ESCOLHA SEU PRÓXIMO ALVO")
        choices = self.mission_manager.get_available_choices()
        for i, c in enumerate(choices):
            ui_console.console.print(f" [{i}] [bold cyan]{c['title']}[/]")
            ui_console.console.print(f"     {c['description']}\n")
        
        sel = ui_console.ask("Selecione o contrato: ")
        try:
            chosen = choices[int(sel)]
            self.mission_manager.select_mission(chosen['id'])
            ui_console.success(f"Contrato aceito: {chosen['title']}")
            # Efeitos da escolha
            if "loud" in chosen['id']:
                self.player.increase_trace(30)
                self.player.increase_alert(1)
                self.player.increase_notoriety(2) # Missões barulhentas dão mais notoriedade
                ui_console.warning("Ação barulhenta! TI em alerta máximo (+30% Trace, +1 Nível de Alerta, +2 Notoriedade).")
        except:
            self.mission_manager.select_mission(choices[0]['id']) # Fallback
            ui_console.warning("Contrato padrão selecionado devido a erro de entrada.")

    def _trigger_game_over(self):
        ui_console.console.clear(); ui_console.error("CONEXÃO PERDIDA / RASTREIO COMPLETO"); StateManager.delete_save(); self.is_running = False; sys.exit()
