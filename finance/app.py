import yfinance
from matplotlib import pyplot

ui_path = yfinance.Ticker("TSLA")

ui_path_info = ui_path.info

# print(ui_path_info["sector"])
# print(ui_path_info["fullTimeEmployees"])
# print(ui_path_info["city"])
# print(ui_path_info["country"])
# print(ui_path_info["website"])
# print(ui_path_info["industry"])
# print(ui_path_info["marketCap"])
# print(ui_path_info["regularMarketOpen"])

# history = ui_path.history(start="2015-10-10")
#
# close = history["Close"]
#
# figure, axis = pyplot.subplots(figsize=(16,9))
# #print(close.index)
# axis.plot(close.index, close, label="close index")
#
# axis.legend()
# pyplot.savefig("plot.png")

rec = ui_path.recommendations
# print(rec)
# print(type(rec))

for item in rec.items():
    if item[0] == "Firm":
        firms = item[1].values.tolist()
    if item[0] == "To Grade":
        to_grade = item[1].values.tolist()

pretty_rec = list(map(lambda x,y: {x: y}, firms, to_grade))
print(pretty_rec)
