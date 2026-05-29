import os, sys, time, random
from entities.player import Player
from entities.network import NetworkNode
from systems.generator import generate_network
from systems.combat import start_hack, run_privesc
from ui import console as ui_console
from ui.market import BlackMarket
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
            
            self._display_node_status()
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
        ui_console.console.clear()
        ui_console.header("SISTEMA DE INVASÃO", "AGENTE GHOST ONLINE")
        ui_console.display_status_table(self.player)
        
        # Filtra e-mails que o jogador "recebeu" (gatilhos atendidos)
        received_emails = [e for e in self.all_emails if self._is_email_triggered(e)]
        unread_count = len([e for e in received_emails if e['id'] not in self.player.read_emails])
        
        if unread_count > 0:
            ui_console.warning(f"VOCÊ TEM {unread_count} E-MAIL(S) NÃO LIDO(S)! [Comando E]")
            
        if self.player.vulnerability_fragments > 0:
            ui_console.system(f"FRAGMENTOS DE ZERO-DAY: {self.player.vulnerability_fragments}/5")
            
        ui_console.console.print(f"\n[bold yellow][MISSÃO]: {self.mission_manager.current_title}[/bold yellow]")
        ui_console.trace_bar(self.player.trace_level)
        print("-" * 60)

    def _is_email_triggered(self, email: dict) -> bool:
        """Verifica se as condições para receber este e-mail foram atendidas."""
        trigger = email.get('trigger_type')
        if trigger == 'mission_active':
            return self.mission_manager.active_mission and self.mission_manager.active_mission['id'] == email.get('mission_id')
        elif trigger == 'notoriety':
            return self.player.notoriety >= email.get('threshold', 0)
        return False

    def _display_node_status(self):
        p_status = "ROOT" if self.current_node.is_root else "USER"
        flags = []
        if self.current_node.is_sniffing: flags.append("Grampeado")
        if self.current_node.is_xss_active: flags.append("Infectado (XSS)")
        if self.current_node.is_under_ransomware: flags.append(f"RANSOMWARE ({self.current_node.ransomware_timer})")
        if self.current_node.has_active_backdoor: flags.append(f"BACKDOOR ({self.current_node.backdoor_timer})")
        if self.current_node.rival_present: flags.append("HACKER RIVAL DETECTADO")
        status_line = f" [{', '.join(flags)}]" if flags else ""
        print(f"\n[NO ATUAL]: {self.current_node.ip} ({self.current_node.node_type}) - {p_status}{status_line}")
        
        if self.current_node.is_root and not self.current_node.is_sniffing: print(" [M] Instalar MITM Sniffer")
        if self.current_node.data_files or self.current_node.ip in self.rival_stolen_files:
            if self.current_node.is_root:
                files = self.current_node.data_files[:]
                if self.current_node.ip in self.rival_stolen_files: files.append("[DADO CRIPTOGRAFADO PELO RIVAL]")
                ui_console.info(f"Arquivos: {', '.join(files)}")
                print(" [D] Baixar arquivos")
            else: print(" [P] Escalar Privilégios (PrivEsc)")
        print("\nConexões detectadas:")
        for i, n in enumerate(self.current_node.connections):
            status = "[ROOT]" if n.is_root else "[USER]" if n.is_hacked else "[LOCKED]"
            if n.rival_present: status += " [!]"
            ui_console.console.print(f" [{i}] -> {n.ip} ({n.node_type}) {status}")
        print("\n [E] Inbox | [L] Logs | [B] Dark Web | [S] Contratos | [Q] Sair | [...] Ajuda")

    def _handle_player_action(self, choice):
        if choice == 'Q': 
            AuditLogger.log("SISTEMA", "Sessão encerrada pelo usuário.")
            StateManager.save_game(self.player.to_dict()); self.is_running = False
        elif choice == 'E': self._display_inbox()
        elif choice == 'L': AuditLogger.display_logs()
        elif choice == 'B': BlackMarket.display_market(self.player)
        elif choice == 'S': self._display_side_missions()
        elif choice == '...': ui_console.display_manual()
        elif choice == '....': self._handle_player_action(AutoHacker.resolve_navigation(self.player, self.current_node, self.mission_manager))
        elif choice == 'M' and self.current_node.is_root and not self.current_node.is_sniffing: self._deploy_mitm()
        elif choice == 'D' and (self.current_node.data_files or self.current_node.ip in self.rival_stolen_files) and self.current_node.is_root: self._execute_data_download()
        elif choice == 'P' and self.current_node.is_hacked and not self.current_node.is_root:
            if run_privesc(self.player, self.current_node): ui_console.wait_for_enter()
        else: self._process_navigation(choice)

    def _display_side_missions(self):
        ui_console.console.clear()
        ui_console.header("QUADRO DE CONTRATOS", "SUBMUNDO")
        
        available = self.mission_manager.available_side_missions
        if not available:
            ui_console.info("Nenhum contrato disponível no momento.")
            ui_console.wait_for_enter(); return

        for i, m in enumerate(available):
            ui_console.console.print(f" [{i}] [bold cyan]{m['title']}[/]")
            ui_console.console.print(f"     {m['description']}")
            ui_console.console.print(f"     Recompensa: [bold gold1]${m['reward_credits']}[/]\n")
        
        sel = ui_console.ask("Aceitar contrato (Enter para voltar): ")
        if sel.isdigit() and int(sel) < len(available):
            mission = available[int(sel)]
            if self.mission_manager.accept_side_mission(mission['id']):
                ui_console.success(f"Contrato aceito: {mission['title']}")
                AuditLogger.log("SISTEMA", f"Contrato secundário aceito: {mission['title']}")
        ui_console.wait_for_enter()

    def _display_inbox(self):
        ui_console.console.clear()
        ui_console.header("INBOX - MENSAGENS CRIPTOGRAFADAS", "GHOST_MAIL_v2.1")
        
        received_emails = [e for e in self.all_emails if self._is_email_triggered(e)]
        if not received_emails:
            ui_console.system("Nenhuma mensagem nova."); ui_console.wait_for_enter(); return

        for e in reversed(received_emails): # Mais recentes primeiro
            status = "[bold green][NOVA][/]" if e['id'] not in self.player.read_emails else "[dim][LIDA][/]"
            ui_console.console.print(f"\n{status} [bold cyan]DE:[/] {e['from']}")
            ui_console.console.print(f"[bold cyan]ASSUNTO:[/] {e['subject']}")
            ui_console.console.print(f"\n{e['body']}")
            
            if e['id'] not in self.player.read_emails:
                self.player.read_emails.append(e['id'])
            print("-" * 40)
            
        ui_console.wait_for_enter()

    def _deploy_mitm(self):
        mitm_s = next((s for s in self.player.scripts if s.id == "mitm"), None)
        if self.player.use_ram(mitm_s.ram_cost):
            self.current_node.is_sniffing = True; self.player.increase_trace(mitm_s.trace_impact)
            ui_console.success("Sniffer instalado."); ui_console.wait_for_enter()

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
                if self.mission_manager.pending_choice:
                    self._handle_mission_branching()
                elif self.mission_manager.is_story_complete: 
                    ui_console.success("\nVOCÊ VENCEU."); self.is_running = False
            else:
                AuditLogger.log("SISTEMA", f"Missão secundária concluída: {m['title']}")
            
            ui_console.wait_for_enter()
            # Verifica se há outra missão concluída (no caso de side quests)
            m = self.mission_manager.check_objective(self.player.collected_data)

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
