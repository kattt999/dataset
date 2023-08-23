import requests
import sqlite3
import time

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.example.com"

conn = sqlite3.connect("stock_alert.db")
cursor = conn.cursor()

cursor.execute("""
    create table if not exists companies(
               id interger primary key,
               symbol text not null,
               alert_price real not null
    )
""")
               
cursor.execute("""
    create table if not exists alerts(
               id interger primary key,
               company_id interger,
               alert_time timestamp default current_timestamp,
               stock_price real not null,
               foreign key(company_id) referneces companies(id)
    )
""")
               
conn.commit()

def fetch_stock_price(symbol):
    url = f"{BASE_URL}/stock/{symbol}/quote?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data["latestPrice"]

def monitor_companies():
    cursor.execute('select * from companies')
    companies = cursor.fetchall()
    for company in companies:
        symbol, alert_price = company[1], company[2]
        current_price = fetch_stock_price(symbol)

        if current_price >= alert_price:
            cursor.execute("insert into alerts (company_id, stock_price) values (?, ?)", (company[0], current_price))
            conn.commit()

def main():
    while True:
        monitor_companies()
        time.sleep(60)

if __name__ == "__main__":
    main()