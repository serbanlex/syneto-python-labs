import yfinance
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from datetime import date

from matplotlib import pyplot

router = APIRouter(prefix="/yfinance")


# GET endpoint for info about every ticker added
@router.get("/tickers")
async def get_all_tickers():
    with open("tickers.txt", "r") as tickers_file:
        # getting all of the file's lines
        file_lines = tickers_file.readlines()

    # here we will store every dictionary
    tickers_list = []

    # taking each line one by one
    for line in file_lines:
        # readlines() includes the \n, so we format it, and it represents the ticker for the current object:
        ticker = line.rstrip()

        # getting ticker info from yfinance
        ticker_info = yfinance.Ticker(ticker).info

        ticker_map = {
            "ticker": ticker,
            "full_name": ticker_info["longName"],
            "employees_number": ticker_info["fullTimeEmployees"],
            "sector": ticker_info["sector"],
            "website": ticker_info["website"],
            "regular_market_price": ticker_info["regularMarketPrice"]
        }

        tickers_list.append(ticker_map)

    return JSONResponse(status_code=200, content=tickers_list)


# POST api endpoint for adding a ticker
@router.post("/tickers/{ticker}")
async def add_ticker(ticker: str):
    # make sure the string given is all in uppercase letters, if not, make them upper
    if ticker.isupper() is False:
        ticker = ticker.upper()

    # check if the added ticker is valid
    ticker_info = yfinance.Ticker(ticker).info

    if ticker_info['logo_url'] == '':
        return JSONResponse(status_code=404, content="Invalid ticker")

    # opening the tickers.txt file for appending (automatically create it if it doesn't exist)
    with open("tickers.txt", "a+", encoding='utf-8') as tickers_file:
        # set the pointer to the beginning, so we can check existing elements
        tickers_file.seek(0)
        file_lines = tickers_file.readlines()

        # checking if the ticker already exists
        for line in file_lines:
            # readlines() includes the \n, so we treat it like that:
            if line.rstrip() == ticker:
                return JSONResponse(status_code=400, content="Ticker already exists!")

        tickers_file.write("%s\n" % ticker)

    return JSONResponse(status_code=200, content="Ticker added successfully!")


# DELETE endpoint in order to delete an existent ticker
@router.delete("/tickers/{ticker_wanted}")
async def delete_ticker(ticker: str):
    # make sure the string given is all in uppercase letters, if not, make them upper
    if ticker.isupper() is False:
        ticker_wanted = ticker.upper()
    else:
        ticker_wanted = ticker
    # store the lines
    try:
        with open("tickers.txt", "r") as tickers_file:
            file_lines = tickers_file.readlines()
    except FileNotFoundError as exc:
        return JSONResponse(status_code=404, content=str(exc))

    deleted_something = 0

    with open("tickers.txt", "w") as tickers_file:
        for line in file_lines:
            # readlines() includes the \n, so we treat it like that:
            if line.rstrip() != ticker_wanted:
                tickers_file.write(line)
            else:
                deleted_something = 1

    if deleted_something == 1:
        return JSONResponse(status_code=200, content="Ticker deleted")
    else:
        return JSONResponse(status_code=404, content="Ticker not found in file")


# GET endpoint for recommendations for an existent ticker
@router.get("/tickers/recommendation/{ticker}")
async def get_recommendations(ticker: str):
    # make sure the string given is all in uppercase letters, if not, make them upper
    if ticker.isupper() is False:
        ticker = ticker.upper()

    ticker_exists = 0

    # see if the ticker exists in our file
    with open("tickers.txt", "r") as tickers_file:
        # set the pointer to the beginning, so we can check existing elements
        tickers_file.seek(0)
        file_lines = tickers_file.readlines()

        for line in file_lines:
            # readlines() includes the \n, so we treat it like that:
            if line.rstrip() == ticker:
                ticker_exists = 1
                break

    if ticker_exists:
        ticker_object = yfinance.Ticker(ticker)
        recommendations = ticker_object.recommendations
        # some tickers may not have recommendations of any kind and we have to treat this
        try:
            recommendations.items()
        except AttributeError:
            return JSONResponse(status_code=404, content="This ticker has no recommendations of any kind")

        for item in recommendations.items():
            if item[0] == "Firm":
                firms = item[1].values.tolist()
            if item[0] == "To Grade":
                to_grade = item[1].values.tolist()

        pretty_recommendations = list(map(lambda x, y: {x: y}, firms, to_grade))
        print(pretty_recommendations)

        return JSONResponse(status_code=200, content=pretty_recommendations)
    else:
        return JSONResponse(status_code=404, content="The given ticker isn't added, please add it for retrieving information.")


# GET endpoint for a graph of the price (close index) between two dates for an existent ticker
@router.get("/tickers/graph/{ticker}", status_code=200)
async def get_ticker_graph(ticker: str, start: str, end: str = None):
    # make sure the string given is all in uppercase letters, if not, make them upper
    if ticker.isupper() is False:
        ticker = ticker.upper()

    ticker_exists = 0

    # if end date doesn't exist, set it to today
    if end is None:
        end = date.today().strftime('%Y-%m-%d')

    # see if the ticker exists in our file
    with open("tickers.txt", "r") as tickers_file:
        # set the pointer to the beginning, so we can check existing elements
        tickers_file.seek(0)
        file_lines = tickers_file.readlines()

        for line in file_lines:
            # readlines() includes the \n, so we treat it like that:
            if line.rstrip() == ticker:
                ticker_exists = 1
                break

    # validate the date
    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)

        if start_date > end_date:
            return JSONResponse(status_code=400, content="Start date can't be older than end date")
        if start_date > date.today() or end_date > date.today():
            return JSONResponse(status_code=400, content="Dates cannot succeed today's date")

    except ValueError:
        return JSONResponse(status_code=400, content="Invalid data string")

    if ticker_exists:
        ticker_object = yfinance.Ticker(ticker)

        history = ticker_object.history(start=start, end=end)

        close = history["Close"]

        figure, axis = pyplot.subplots(figsize=(16, 9))

        # print(close.index)
        axis.plot(close.index, close, label="close index")

        axis.legend()
        pyplot.savefig("plot.png")
        return FileResponse("plot.png", media_type="image/png")

    else:
        return JSONResponse(status_code=404, content="The given ticker isn't added, please add it for retrieving information.")
