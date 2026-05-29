import unittest
import sys
import os

# Adiciona o caminho src para que os testes encontrem os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from entities.network import NetworkNode
from core.game_loop import GameLoop

class TestSupplyChain(unittest.TestCase):
    def test_backdoor_cascade_effect(self):
        # Setup
        supplier = NetworkNode("1.1.1.1", "Software Supplier")
        target = NetworkNode("2.2.2.2", "Mainframe")
        supplier.connect(target)
        
        supplier.is_supply_chain_infected = True
        supplier.backdoor_timer = 1
        
        loop = GameLoop()
        loop.all_network_nodes = [supplier, target]
        
        # Simula o processamento de um turno
        loop._process_passive_actions()
        
        self.assertEqual(supplier.backdoor_timer, 0)
        self.assertTrue(target.is_hacked, "O alvo deveria ter sido hackeado via Supply Chain!")
        self.assertTrue(target.is_root, "O alvo deveria ter acesso ROOT via Supply Chain!")

if __name__ == "__main__":
    unittest.main()
