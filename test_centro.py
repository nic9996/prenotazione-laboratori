import unittest

from prenotazioni import Centro, Laboratorio, LaboratorioNonTrovato

class TestCentro(unittest.TestCase):
    # `aggiungi_laboratorio` rifiuta un codice duplicato con `ValueError`; 
    # `laboratorio` solleva `LaboratorioNonTrovato` per un codice inesistente;
    def test_laboratorio(self):
        centro = Centro()
        laboratorio_a = Laboratorio("LAB001", "Meccanica", 15)
        laboratorio_b = Laboratorio("LAB001", "Chimica", 20)
        centro.aggiungi_laboratorio(laboratorio_a)
        with self.assertRaises(ValueError):
            centro.aggiungi_laboratorio(laboratorio_b)
        with self.assertRaises(LaboratorioNonTrovato):
            centro.laboratorio("XXXXXX")