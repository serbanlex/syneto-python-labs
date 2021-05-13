import sqlite3
from sqlite3 import Error
import requests

def create_connection(file: str):
    connection = None
    try:
        connection = sqlite3.connect(file)
    except Error as e:
        print("Error: ", e)

    return connection

con = create_connection("alex.db")
cursor = con.cursor()

def get_db_data():
    cursor.execute("SELECT * FROM TICKERS")
    db_data = cursor.fetchall()

    for db_row in db_data:
        print(db_row)

# cursor.execute("CREATE TABLE USERS (id INTEGER PRIMARY KEY, name TEXT)")

# cursor.execute("INSERT into USERS (name) values ('marius')")
#
# con.commit()
#
# cursor.execute("SELECT * FROM USERS")
#
# con.commit()
#db_rows = cursor.fetchall()

# for row in db_rows:
#     print(row)

def insert_in_db(file: str)->None:
    with open(file) as f:
        data = f.readlines()

    for line in data:
        formated_line = line.replace('\n', '')
        cursor.execute(f"INSERT INTO TICKERS (name) values ('{formated_line}')")

    con.commit()

# cursor.execute("CREATE TABLE TICKERS (id INTEGER PRIMARY KEY, name VARCHAR(20))")

insert_in_db("../finance/tickers.txt")

cursor.execute("SELECT * FROM TICKERS")


def delete_from_db() -> None:
    cursor.execute("DELETE FROM TICKERS WHERE name = 'TSLA'")

def delete_all_db() -> None:
    cursor.execute("DELETE FROM TICKERS")

# delete_from_db()

# get_db_data()

def update_db(id: int, name: str) -> None:
    cursor.execute(f"UPDATE TICKERS SET name='{name}' WHERE id = '{id}'")

# update_db(50, "ceva")
# get_db_data()

# delete_all_db()
get_db_data()

class TickerInfo:
    def create_table(self):
        cursor.execute("CREATE TABLE TickerInfo (id integer PRIMARY KEY, num_employees INTEGER, sector TEXT, web TEXT, price INTEGER)")

    def insert(self, nr, sector, web, price):
        cursor.execute("INSERT INTO TickerInfo (num_employees, sector, web, price) VALUES ('{}', '{}', '{}', '{}')".format(nr, sector, web, price))

ticker_info = TickerInfo()

response = requests.get("http://127.0.0.1/get_info/", params={'ticker': "TSLA"})
response.json()
print(response)


