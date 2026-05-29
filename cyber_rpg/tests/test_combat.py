import unittest
import sys
import os

# Garante que a pasta 'src' está no caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestCombatIntegrity(unittest.TestCase):
    def test_combat_module_loading(self):
        """Verifica se o módulo de combate pode ser importado sem erros de dependência."""
        try:
            import systems.combat
            import ui.console
            import entities.player
            import entities.network
            module_loaded = True
        except ImportError as e:
            print(f"Erro de importação: {e}")
            module_loaded = False
        
        self.assertTrue(module_loaded, "O módulo de combate ou suas dependências não puderam ser carregados.")

if __name__ == "__main__":
    unittest.main()
