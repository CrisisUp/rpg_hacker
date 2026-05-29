import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from systems.missions import MissionManager

class TestMissions(unittest.TestCase):
    def setUp(self):
        self.manager = MissionManager()

    def test_initial_mission(self):
        """Verifica se a primeira missão é carregada."""
        self.assertIsNotNone(self.manager.active_mission)
        self.assertEqual(self.manager.current_title, "Fase 1: Infiltração Inicial")

    def test_mission_branching(self):
        """Verifica se a coleta do arquivo correto abre ramificações."""
        target_file = self.manager.active_mission['required_file']
        
        # Coleta o arquivo da missão 1
        completed = self.manager.check_objective([target_file])
        
        self.assertIsNotNone(completed)
        self.assertTrue(self.manager.pending_choice, "Deveria estar pendente de escolha!")
        
        choices = self.manager.get_available_choices()
        self.assertEqual(len(choices), 2)
        
        # Simula escolha da missão silenciosa
        self.manager.select_mission("mission_02_silent")
        self.assertFalse(self.manager.pending_choice)
        self.assertEqual(self.manager.active_mission['id'], "mission_02_silent")

if __name__ == "__main__":
    unittest.main()
