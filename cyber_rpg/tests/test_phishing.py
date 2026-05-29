import unittest
import sys
import os
from unittest.mock import patch

# Adiciona o caminho src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from entities.player import Player
from entities.network import NetworkNode
from systems.combat import _run_social_engineering_game

class TestPhishing(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHacker")

    @patch('ui.console.ask', return_value='0')
    @patch('random.choice')
    def test_phishing_success(self, mock_choice, mock_ask):
        # Força o primeiro cenário (Estagiário) e a primeira opção (Sucesso)
        mock_choice.return_value = {
            "persona": "Test", "context": "Test", "prompt": "Test",
            "options": [{"text": "Success", "success": True, "trace": 10}]
        }
        
        result = _run_social_engineering_game(self.player)
        self.assertEqual(result, 100)
        self.assertEqual(self.player.trace_level, 10)

    @patch('ui.console.ask', return_value='0')
    @patch('random.choice')
    def test_phishing_failure(self, mock_choice, mock_ask):
        # Força falha
        mock_choice.return_value = {
            "persona": "Test", "context": "Test", "prompt": "Test",
            "options": [{"text": "Fail", "success": False, "trace": 20}]
        }
        
        result = _run_social_engineering_game(self.player)
        self.assertEqual(result, 0)
        self.assertEqual(self.player.trace_level, 20)
        self.assertLess(self.player.connection_stability, 100)

if __name__ == "__main__":
    unittest.main()
