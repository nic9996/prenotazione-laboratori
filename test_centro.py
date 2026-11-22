import unittest
from datetime import date, timedelta

from prenotazioni import (
    ORIZZONTE_GIORNI,
    Centro,
    DataNonAmmessa,
    Laboratorio,
    LaboratorioNonTrovato,
    Sessione,
    SessioneNonTrovata,
)


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
        giorno2 = date(2026, 11, 20)  # è un venerdì
        oggi = date(2026, 11, 22)
        centro = Centro()
        laboratorio = Laboratorio("LAB001", "Meccanica", 15)
        centro.aggiungi_laboratorio(laboratorio)
        # test data passata
        sessione = Sessione(
            "LAB001",
            giorno1,
            "09:00",
            "12:00",
            "Giovanni",
            13,
        )
        with self.assertRaises(DataNonAmmessa):
            centro.prenota(sessione, oggi=oggi)
        # test venerdì
        sessione = Sessione(
            "LAB001",
            giorno2,
            "09:00",
            "12:00",
            "Giovanni",
            13,
        )
        with self.assertRaises(DataNonAmmessa):
            centro.prenota(sessione, oggi=oggi)
        # test data oltre l'orizzonte
        sessione = Sessione(
            "LAB001",
            oggi + timedelta(days=ORIZZONTE_GIORNI + 1),
            "09:00",
            "12:00",
            "Giovanni",
            13,
        )
        with self.assertRaises(DataNonAmmessa):
            centro.prenota(sessione, oggi=oggi)
        # accettazione data di oggi
        sessione = Sessione("LAB001", oggi, "09:00", "12:00", "Giovanni", 13)
        centro.prenota(sessione, oggi=oggi)
        # accettazione data limite di ORIZZONTE GIORNI
        sessione = Sessione(
            "LAB001",
            oggi + timedelta(days=ORIZZONTE_GIORNI),
            "09:00",
            "12:00",
            "Giovanni",
            13,
        )
        centro.prenota(sessione, oggi=oggi)

    def test_id(self):
        # gli id assegnati da `prenota` sono progressivi e non vengono riutilizzati
        # dopo una cancellazione;
        giorno = date(2026, 11, 24)
        oggi = date(2026, 11, 22)
        centro = Centro()
        laboratorio = Laboratorio("LAB001", "Meccanica", 13)
        centro.aggiungi_laboratorio(laboratorio)
        sessione_a = Sessione("LAB001", giorno, "09:00", "12:00", "Giovanni", 10)
        prenotazione1 = centro.prenota(sessione_a, oggi)
        sessione_b = Sessione("LAB001", giorno, "12:00", "14:00", "Giovanni", 10)
        prenotazione2 = centro.prenota(sessione_b, oggi)
        centro.cancella(prenotazione1)
        sessione_c = Sessione("LAB001", giorno, "14:00", "14:30", "Giovanni", 10)
        prenotazione3 = centro.prenota(sessione_c, oggi)
        self.assertEqual(prenotazione1, 1)
        self.assertEqual(prenotazione2, 2)
        self.assertEqual(prenotazione3, 3)

    def test_id_inesistente(self):
        # `cancella` e `sessione` sollevano `SessioneNonTrovata` per un id
        # inesistente;
        centro = Centro()
        with self.assertRaises(SessioneNonTrovata):
            centro.cancella("x")
        with self.assertRaises(SessioneNonTrovata):
            centro.sessione("x")

    def test_sessioni_del_giorno(self):
        # `sessioni_del_giorno` restituisce le sessioni ordinate per orario di
        # inizio e, se indicato il laboratorio, solo quelle del laboratorio. I dati
        # vanno scelti in modo che l'ordine per orario sia diverso da quello per
        # codice: altrimenti il test non distingue i due comportamenti.
        giorno = date(2026, 11, 26)
        oggi = date(2026, 11, 22)
        centro = Centro()
        laboratorio_a = Laboratorio("LAB001", "Meccanica", 13)
        centro.aggiungi_laboratorio(laboratorio_a)
        laboratorio_b = Laboratorio("LAB002", "Chimica", 13)
        centro.aggiungi_laboratorio(laboratorio_b)
        sessione_b = Sessione("LAB002", giorno, "12:00", "14:00", "Giovanni", 10)
        centro.prenota(sessione_b, oggi)
        sessione_a = Sessione("LAB001", giorno, "09:00", "12:00", "Giovanni", 10)
        centro.prenota(sessione_a, oggi)

        tutti = centro.sessioni_del_giorno(giorno)
        filtrati = centro.sessioni_del_giorno(giorno, "LAB001")

        self.assertEqual([x.id for x in tutti], [2, 1])
        self.assertEqual([x.id for x in filtrati], [2])
