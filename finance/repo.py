class TickerRepository:
    def __init__(self, file_name: str = "tickers.txt"):
        self.file_name = file_name

    def add(self, ticker:str):
        with open(self.file_name, "a") as file:
            file.write(ticker + "\n")

    def delete(self, ticker:str):
        # make sure the string given is all in uppercase letters, if not, make them upper
        if ticker.isupper() is False:
            ticker_wanted = ticker.upper()
        else:
            ticker_wanted = ticker
        # store the lines
        try:
            with open(self.file_name, "r") as tickers_file:
                file_lines = tickers_file.readlines()
        except FileNotFoundError as exc:
            return "File not found"

        deleted_something = 0

        with open(self.file_name, "w") as tickers_file:
            for line in file_lines:
                # readlines() includes the \n, so we treat it like that:
                if line.rstrip() != ticker_wanted:
                    tickers_file.write(line)
                else:
                    deleted_something = 1

    def get_all(self) ->list[str]:
        with open(self.file_name) as file:
            lines = file.readlines()
        #     lines = file.read()
        # return lines.split("\n")[:-1]

        return list(map(lambda x: x.removesuffix("\n"), lines))

        # list = []
        # for line in lines:
        #     list.append(line.removesuffix("\n"))
        #
        # return list
