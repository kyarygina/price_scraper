from prefect import flow, task
from datetime import datetime
from db.database import init_db
import sqlite3
from scraper.mvideo import get_price as mvideo_price
from scraper.citilink import get_price as citilink_price

DB_PATH = "data/prices.db"


@task
def collect_data():
    data = [
        {"shop": "mvideo", "price": mvideo_price()},
        {"shop": "citilink", "price": citilink_price()},
    ]

    for d in data:
        d["timestamp"] = datetime.now()

    return data


@task
def save_data(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for d in data:
        cursor.execute(
            "INSERT INTO prices (shop, price, timestamp) VALUES (?, ?, ?)",
            (d["shop"], int(d["price"]), str(d["timestamp"]))
        )

    conn.commit()
    conn.close()


@flow
def main():
    init_db()

    data = collect_data()
    save_data(data)


if __name__ == "__main__":
    main()
