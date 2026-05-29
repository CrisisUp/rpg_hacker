import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from systems.generator import generate_network
from entities.network import NetworkNode

class TestGenerator(unittest.TestCase):
    def test_network_generation(self):
        """Verifica se o gerador cria um grafo de servidores válido."""
        gateway = generate_network(nodes_count=5)
        self.assertIsInstance(gateway, NetworkNode)
        self.assertEqual(gateway.ip, "192.168.0.1")
        
        # Verifica se o Gateway tem conexões (grafo não isolado)
        self.assertGreater(len(gateway.connections), 0)

if __name__ == "__main__":
    unittest.main()
