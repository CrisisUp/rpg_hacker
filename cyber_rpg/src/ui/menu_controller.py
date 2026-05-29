from ui import console
from ui.market import BlackMarket

class MenuController:
    """Gerencia a exibição e navegação dos menus fora de combate."""
    
    @staticmethod
    def display_interface(player, mission_manager, unread_emails_count):
        console.console.clear()
        console.header("SISTEMA DE INVASÃO", "AGENTE GHOST ONLINE")
        console.display_status_table(player)
        
        if unread_emails_count > 0:
            console.warning(f"VOCÊ TEM {unread_emails_count} E-MAIL(S) NÃO LIDO(S)! [Comando E]")
            
        if player.vulnerability_fragments > 0:
            console.system(f"FRAGMENTOS DE ZERO-DAY: {player.vulnerability_fragments}/5")
            
        current_title = mission_manager.current_title if mission_manager else "SISTEMA LIVRE"
        console.console.print(f"\n[bold yellow][MISSÃO]: {current_title}[/bold yellow]")
        console.trace_bar(player.trace_level)
        print("-" * 60)

    @staticmethod
    def display_node_status(current_node, rival_stolen_files):
        p_status = "ROOT" if current_node.is_root else "USER"
        flags = []
        if current_node.is_sniffing: flags.append("Grampeado")
        if current_node.is_xss_active: flags.append("Infectado (XSS)")
        if current_node.is_under_ransomware: flags.append(f"RANSOMWARE ({current_node.ransomware_timer})")
        if current_node.has_active_backdoor: flags.append(f"BACKDOOR ({current_node.backdoor_timer})")
        if current_node.rival_present: flags.append("HACKER RIVAL DETECTADO")
        status_line = f" [{', '.join(flags)}]" if flags else ""
        print(f"\n[NO ATUAL]: {current_node.ip} ({current_node.node_type}) - {p_status}{status_line}")
        
        if current_node.is_root and not current_node.is_sniffing: print(" [M] Instalar MITM Sniffer")
        if current_node.data_files or current_node.ip in rival_stolen_files:
            if current_node.is_root:
                files = current_node.data_files[:]
                if current_node.ip in rival_stolen_files: files.append("[DADO CRIPTOGRAFADO PELO RIVAL]")
                console.info(f"Arquivos: {', '.join(files)}")
                print(" [D] Baixar arquivos")
            else: print(" [P] Escalar Privilégios (PrivEsc)")
            
        print("\nConexões detectadas:")
        for i, n in enumerate(current_node.connections):
            status = "[ROOT]" if n.is_root else "[USER]" if n.is_hacked else "[LOCKED]"
            if n.rival_present: status += " [!]"
            console.console.print(f" [{i}] -> {n.ip} ({n.node_type}) {status}")
        print("\n [E] Inbox | [L] Logs | [B] Dark Web | [S] Contratos | [Q] Sair | [...] Ajuda")

    @staticmethod
    def display_side_missions(mission_manager, audit_logger):
        console.console.clear()
        console.header("QUADRO DE CONTRATOS", "SUBMUNDO")
        
        available = mission_manager.available_side_missions
        if not available:
            console.info("Nenhum contrato disponível no momento.")
            console.wait_for_enter(); return

        for i, m in enumerate(available):
            console.console.print(f" [{i}] [bold cyan]{m['title']}[/]")
            console.console.print(f"     {m['description']}")
            console.console.print(f"     Recompensa: [bold gold1]${m['reward_credits']}[/]\n")
        
        sel = console.ask("Aceitar contrato (Enter para voltar): ")
        if sel.isdigit() and int(sel) < len(available):
            mission = available[int(sel)]
            if mission_manager.accept_side_mission(mission['id']):
                console.success(f"Contrato aceito: {mission['title']}")
                audit_logger.log("SISTEMA", f"Contrato secundário aceito: {mission['title']}")
        console.wait_for_enter()

    @staticmethod
    def display_inbox(received_emails, player):
        console.console.clear()
        console.header("INBOX - MENSAGENS CRIPTOGRAFADAS", "GHOST_MAIL_v2.1")
        
        if not received_emails:
            console.system("Nenhuma mensagem nova."); console.wait_for_enter(); return

        for e in reversed(received_emails): # Mais recentes primeiro
            status = "[bold green][NOVA][/]" if e['id'] not in player.read_emails else "[dim][LIDA][/]"
            console.console.print(f"\n{status} [bold cyan]DE:[/] {e['from']}")
            console.console.print(f"[bold cyan]ASSUNTO:[/] {e['subject']}")
            console.console.print(f"\n{e['body']}")
            
            if e['id'] not in player.read_emails:
                player.read_emails.append(e['id'])
            print("-" * 40)
            
        console.wait_for_enter()

    @staticmethod
    def open_black_market(player):
        BlackMarket.display_market(player)

    @staticmethod
    def display_manual():
        console.display_manual()
