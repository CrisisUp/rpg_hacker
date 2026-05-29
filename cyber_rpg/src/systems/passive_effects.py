import random
from ui import console as ui_console
from entities.network import NetworkNode

class PassiveEffectManager:
    """Gerencia efeitos que ocorrem automaticamente a cada turno na rede."""
    
    def __init__(self, player):
        self.player = player

    def process_all(self, all_nodes):
        self._process_mitm(all_nodes)
        self._process_xss(all_nodes)
        self._process_ransomware(all_nodes)
        self._process_supply_chain(all_nodes)

    def _process_mitm(self, nodes):
        for node in [n for n in nodes if n.is_sniffing]:
            if random.random() < 0.20:
                gain = random.randint(50, 150)
                self.player.add_credits(gain)
                ui_console.success(f"MITM {node.ip}: +${gain}")
            self.player.increase_trace(1)

    def _process_xss(self, nodes):
        for node in [n for n in nodes if n.is_xss_active]:
            if random.random() < 0.15:
                new_ip = f"172.16.0.{random.randint(100, 254)}"
                ws = NetworkNode(new_ip, "Employee Workstation")
                ws.data_files = ["personal_secrets.txt"]
                node.connect(ws)
                nodes.append(ws)
                ui_console.warning(f"\n[XSS] Workstation detectada: {ws.ip}")

    def _process_ransomware(self, nodes):
        for node in nodes:
            if node.is_under_ransomware:
                node.ransomware_timer -= 1
                self.player.increase_trace(10)
                ui_console.warning(f"[RANSOMWARE] Criptografando {node.ip}... TI em alerta! (+10% Trace)")
                
                if node.ransomware_timer <= 0:
                    node.is_corrupted = True
                    node.data_files = []
                    resgate = random.randint(2000, 5000)
                    self.player.add_credits(resgate)
                    ui_console.header("RESGATE RECEBIDO", f"+${resgate}")
                    ui_console.success(f"O servidor {node.ip} foi totalmente criptografado. Pagamento via Monero.")

    def _process_supply_chain(self, nodes):
        for node in [n for n in nodes if n.has_active_backdoor]:
            node.backdoor_timer -= 1
            if node.backdoor_timer <= 0:
                omnicorp_targets = [n for n in node.connections if not n.is_hacked and "Supplier" not in n.node_type]
                if omnicorp_targets:
                    target = random.choice(omnicorp_targets)
                    target.is_hacked = True
                    target.is_root = True
                    ui_console.success(f"\n[SUPPLY CHAIN] Backdoor ativado! {target.ip} sob controle (ROOT).")
                else:
                    ui_console.system(f"\n[SUPPLY CHAIN] Backdoor em {node.ip} expirou sem alvos.")
