import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from systems.missions import MissionManager

class TestMissions(unittest.TestCase):
    def setUp(self):
        # Como o MissionManager carrega o JSON real, vamos garantir que ele inicializa
        self.manager = MissionManager()

    def test_initial_mission(self):
        """Verifica se a primeira missão é carregada."""
        self.assertIsNotNone(self.manager.active_mission)
        self.assertEqual(self.manager.current_title, "O Despertar do Hacker")

    def test_mission_completion(self):
        """Verifica se a coleta do arquivo correto completa a missão."""
        target_file = self.manager.active_mission['required_file']
        
        # Simula o jogador coletando o arquivo
        completed = self.manager.check_objective([target_file])
        
        self.assertIsNotNone(completed)
        self.assertEqual(completed['required_file'], target_file)
        # Deve ter avançado para a próxima
        self.assertNotEqual(self.manager.current_title, "O Despertar do Hacker")

if __name__ == "__main__":
    unittest.main()
