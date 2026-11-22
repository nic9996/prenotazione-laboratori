import unittest
from datetime import date, timedelta

from prenotazioni import Centro, Laboratorio, LaboratorioNonTrovato, Sessione, DataNonAmmessa, ORIZZONTE_GIORNI

class TestCentro(unittest.TestCase):
    # `aggiungi_laboratorio` rifiuta un codice duplicato con `ValueError`; 
    # `laboratorio` solleva `LaboratorioNonTrovato` per un codice inesistente;
    def test_laboratori(self):
        centro = Centro()
        laboratorio_a = Laboratorio("LAB001", "Meccanica", 15)
        laboratorio_b = Laboratorio("LAB001", "Chimica", 20)
        centro.aggiungi_laboratorio(laboratorio_a)
        with self.assertRaises(ValueError):
            centro.aggiungi_laboratorio(laboratorio_b)
        with self.assertRaises(LaboratorioNonTrovato):
            centro.laboratorio("XXXXXX")

    def test_data_non_ammessa(self):
        # `prenota` solleva `DataNonAmmessa` per una data passata, un venerdì e una
        #  data oltre l'orizzonte, e accetta la data di oggi;
        giorno1 = date(2026, 11, 8)
        giorno2 = date(2026, 11, 20) # è un venerdì
        oggi = date(2026, 11, 22)
        centro = Centro()
        laboratorio = Laboratorio("LAB001", "Meccanica", 15)
        centro.aggiungi_laboratorio(laboratorio)
        sessione = Sessione("LAB001", giorno1, "09:00", "12:00", "Giovanni", 13)
        with self.assertRaises(DataNonAmmessa):
            centro.prenota(sessione, oggi=oggi)
        sessione = Sessione("LAB001", giorno2, "09:00", "12:00", "Giovanni", 13)
        with self.assertRaises(DataNonAmmessa):
            centro.prenota(sessione, oggi=oggi)
        sessione = Sessione("LAB001", oggi + timedelta(days=ORIZZONTE_GIORNI + 1), "09:00", "12:00", "Giovanni", 13)
        with self.assertRaises(DataNonAmmessa):
            centro.prenota(sessione, oggi=oggi)
        sessione = Sessione("LAB001", oggi, "09:00", "12:00", "Giovanni", 13)
        centro.prenota(sessione, oggi=oggi)
        sessione = Sessione("LAB001", oggi + timedelta(days=ORIZZONTE_GIORNI), "09:00", "12:00", "Giovanni", 13)
        centro.prenota(sessione, oggi=oggi)