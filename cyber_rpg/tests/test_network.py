import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from entities.network import NetworkNode

class TestNetwork(unittest.TestCase):
    def test_node_connection_bidirectional(self):
        """Garante que ao conectar A em B, B também conhece A."""
        node_a = NetworkNode("1.1.1.1", "Type A")
        node_b = NetworkNode("2.2.2.2", "Type B")
        
        node_a.connect(node_b)
        
        self.assertIn(node_b, node_a.connections)
        self.assertIn(node_a, node_b.connections)

    def test_prevent_duplicate_connections(self):
        """Garante que o sistema não cria conexões duplicadas entre os mesmos nós."""
        node_a = NetworkNode("1.1.1.1", "Type A")
        node_b = NetworkNode("2.2.2.2", "Type B")
        
        node_a.connect(node_b)
        node_a.connect(node_b) # Tentativa duplicada
        
        self.assertEqual(len(node_a.connections), 1)

if __name__ == "__main__":
    unittest.main()
