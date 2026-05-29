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

class TestRansomware(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHacker")
        self.ransom_script = HackingScript(
            id="ransomware", name="Ransom_X", ram_cost=6, 
            damage=0, trace_impact=20, price=800, description="Test"
        )
        self.player.add_script(self.ransom_script)

    @patch('ui.console.ask', return_value='1') # Escolhe Extorsão Padrão
    def test_ransomware_activation(self, mock_ask):
        node = NetworkNode("1.1.1.1", "File Server")
        # O índice é 0 pois é o único script
        result = _execute_script_logic(self.player, 0, node)
        
        self.assertEqual(result, 100)
        self.assertEqual(node.ransomware_timer, 5)
        self.assertEqual(self.player.trace_level, 20)

    @patch('ui.console.ask', return_value='2') # Escolhe Extorsão Dupla
    def test_double_extortion(self, mock_ask):
        node = NetworkNode("1.1.1.1", "File Server")
        _execute_script_logic(self.player, 0, node)
        
        # Sucesso na extorsão dupla: créditos > 0 e trace aumentado (>20 do script + 40 da extorsão)
        self.assertGreater(self.player.credits, 0)
        self.assertEqual(self.player.trace_level, 60)

    def test_ransom_payment_in_loop(self):
        loop = GameLoop()
        loop.player = self.player
        node = NetworkNode("2.2.2.2", "Mainframe")
        node.ransomware_timer = 1
        loop.all_network_nodes = [node]
        
        initial_credits = self.player.credits
        initial_trace = self.player.trace_level
        
        loop._process_passive_actions()
        
        self.assertEqual(node.ransomware_timer, 0)
        self.assertTrue(node.is_corrupted)
        self.assertGreater(self.player.credits, initial_credits, "Deveria ter recebido o resgate!")
        self.assertEqual(self.player.trace_level, initial_trace + 10, "Trace deveria ter aumentado no turno!")

if __name__ == "__main__":
    unittest.main()
