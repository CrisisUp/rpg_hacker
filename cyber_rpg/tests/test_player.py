import unittest
import sys
import os

# Adiciona o caminho src para que os testes encontrem os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from entities.player import Player
from entities.script import HackingScript

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHacker")
        self.test_script = HackingScript(
            id="test", name="TestScript", ram_cost=4, 
            damage=10, trace_impact=5, price=100, description="Desc"
        )

    def test_initial_stats(self):
        """Garante que o jogador começa com os valores corretos."""
        self.assertEqual(self.player.handle, "TestHacker")
        self.assertEqual(self.player.current_ram, 16)
        self.assertEqual(self.player.credits, 0)
        self.assertEqual(self.player.read_emails, [])

    def test_to_from_dict(self):
        """Testa serialização e desserialização do jogador."""
        self.player.read_emails.append("mission_01")
        data = self.player.to_dict()
        self.assertIn("read_emails", data)
        self.assertEqual(data["read_emails"], ["mission_01"])
        
        new_player = Player("New")
        new_player.from_dict(data, [])
        self.assertEqual(new_player.read_emails, ["mission_01"])

    def test_use_ram_success(self):
        """Testa consumo de RAM com sucesso."""
        result = self.player.use_ram(4)
        self.assertTrue(result)
        self.assertEqual(self.player.current_ram, 12)

    def test_use_ram_failure(self):
        """Testa se o sistema impede o uso de RAM acima do limite."""
        result = self.player.use_ram(20)
        self.assertFalse(result)
        self.assertEqual(self.player.current_ram, 16)

    def test_receive_loot(self):
        """Testa se o recebimento de arquivos e créditos funciona."""
        self.player.receive_loot("secret.txt", 150)
        self.assertIn("secret.txt", self.player.collected_data)
        self.assertEqual(self.player.credits, 150)
        self.assertGreater(self.player.exp, 0)

    def test_trace_management(self):
        """Testa se o rastreio aumenta e diminui dentro dos limites."""
        self.player.increase_trace(50)
        self.assertEqual(self.player.trace_level, 50)
        self.player.increase_trace(100) # Deve limitar em 100
        self.assertEqual(self.player.trace_level, 100)
        self.player.reduce_trace(200) # Deve limitar em 0
        self.assertEqual(self.player.trace_level, 0)

if __name__ == "__main__":
    unittest.main()
