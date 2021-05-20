class TickerRepository:
    def __init__(self, file_name: str = "tickers.txt"):
        self.file_name = file_name

    def add(self, ticker:str):
        with open(self.file_name, "a") as file:
            file.write(ticker + "\n")

