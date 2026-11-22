import unittest
from datetime import date

from prenotazioni import Sessione

class TestSessione(unittest.TestCase):
    def test_orario_di_apertura(self):
        Sessione("SNE001", date(2026, 11, 23), "08:00", "10:00", "Giovanni", 25)