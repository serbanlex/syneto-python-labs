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

    @unittest.skip("This is incomplete")
    def test_skip(self):
        x = 5
        self.assertEqual(10, x)

    def test_delete(self):
        self.repo.add("TSLA")
        self.repo.delete("TSLA")

        with open(self.txt) as file:
            self.assertEqual("", file.read())

    def test_get(self):
        self.repo.add("TSLA")
        self.repo.add("AAPL")
        self.repo.add("PATH")

        tickers = self.repo.get_all()
        expected_tickers = ["TSLA", "AAPL", "PATH"]

        self.assertEqual(expected_tickers, tickers)