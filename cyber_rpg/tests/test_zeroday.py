import unittest
import sys
import os
from unittest.mock import patch

# Adiciona o caminho src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from entities.player import Player
from entities.network import NetworkNode
from core.game_loop import GameLoop
from systems.combat import _execute_script_logic
from entities.script import HackingScript

class TestZeroDay(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHacker")
        self.zeroday_script = HackingScript(
            id="zeroday", name="ZeroDay", ram_cost=0, 
            damage=999, trace_impact=0, price=1000, description="Test"
        )
        self.player.add_script(self.zeroday_script)

    def test_zeroday_consumption(self):
        node = NetworkNode("1.1.1.1", "Mainframe")
        # O índice do script zeroday é 0 pois é o único adicionado no setUp
        result = _execute_script_logic(self.player, 0, node)
        
        self.assertEqual(result, 999)
        self.assertEqual(len(self.player.scripts), 0, "O Zero-Day deveria ter sido removido após o uso!")

    def test_fragment_compilation(self):
        loop = GameLoop()
        loop.player = Player("DevHacker")
        loop.player.vulnerability_fragments = 4
        loop.current_node = NetworkNode("1.2.3.4", "Vault")
        loop.current_node.is_root = True
        loop.current_node.data_files = ["vulnerability_fragment_99.bin"]
        
        # Simula o download do 5º fragmento
        with patch('ui.console.wait_for_enter'), patch('systems.loader.get_all_scripts') as mock_scripts:
            mock_scripts.return_value = [self.zeroday_script]
            loop._execute_data_download()
            
        self.assertEqual(loop.player.vulnerability_fragments, 0)
        self.assertTrue(any(s.id == "zeroday" for s in loop.player.scripts), "Deveria ter compilado o Zero-Day!")

if __name__ == "__main__":
    unittest.main()
