import os
import unittest
from repo import TickerRepository

class TestDelete (unittest.TestCase):
    def test_sum(self):
        x = 2+5
        self.assertEqual(7, x)

    def test_add_ticker(self):
        self.repo.add("TSLA")
        self.repo.add("AAPL")

        with open(self.txt) as file:
            self.assertEqual(file.read(), "TSLA\nAAPL\n")

    def setUp(self) -> None:
        self.txt = "test_tickers.txt"
        self.repo = TickerRepository(self.txt)

    def tearDown(self) -> None:
        try:
            os.remove(self.txt)
        except FileNotFoundError as e:
            pass