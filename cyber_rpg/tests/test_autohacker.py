import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from systems.auto_hacker import AutoHacker
from entities.player import Player
from entities.network import NetworkNode
from systems.missions import MissionManager

class TestAutoHacker(unittest.TestCase):
    def setUp(self):
        self.player = Player("GhostTest")
        self.node = NetworkNode("1.1.1.1", "TestNode")
        # Simula o MissionManager
        self.mission_manager = MissionManager()

    def test_decision_priority_download(self):
        """IA deve sempre priorizar baixar arquivos se eles existirem."""
        self.node.data_files = ["target.txt"]
        decision = AutoHacker.resolve_navigation(self.player, self.node, self.mission_manager)
        self.assertEqual(decision, 'D')

    def test_combat_priority_reboot(self):
        """IA deve priorizar Reboot se a RAM estiver crítica."""
        self.player.current_ram = 1 # RAM insuficiente para scripts
        action, sub = AutoHacker.resolve_combat(self.player, 10)
        self.assertEqual(action, "3") # 3 é o código para Reboot

    def test_combat_priority_stealth(self):
        """IA deve priorizar ProxyHop se o rastreio estiver alto."""
        from entities.script import HackingScript
        # Dá um script de proxy para o player
        self.player.scripts = [HackingScript("proxy_hop", "Proxy", 2, 0, -20, 0, "Desc")]
        self.player.increase_trace(80) # Rastreio perigoso
        
        action, sub = AutoHacker.resolve_combat(self.player, 10)
        self.assertEqual(action, "2") # Usar script
        self.assertEqual(sub, "0") # Índice do proxy

if __name__ == "__main__":
    unittest.main()
