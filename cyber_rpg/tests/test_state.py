import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.state import StateManager

class TestState(unittest.TestCase):
    def setUp(self):
        self.test_save = "data/test_save.json"
        StateManager.SAVE_FILE = self.test_save
        self.mock_data = {"handle": "Test", "credits": 500}

    def tearDown(self):
        """Limpa o arquivo de teste após cada execução."""
        if os.path.exists(self.test_save):
            os.remove(self.test_save)

    def test_save_and_load_integrity(self):
        """Garante que os dados salvos são exatamente os mesmos carregados."""
        StateManager.save_game(self.mock_data)
        loaded_data = StateManager.load_game()
        self.assertEqual(loaded_data["handle"], "Test")
        self.assertEqual(loaded_data["credits"], 500)

    def test_load_non_existent_file(self):
        """Verifica se o sistema lida bem com a ausência de um save."""
        data = StateManager.load_game()
        self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()
