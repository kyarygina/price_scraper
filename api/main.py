from fastapi import FastAPI, Query, HTTPException
import sqlite3
from typing import Optional

app = FastAPI(title="Price Scraper API")


@app.get("/")
def root():
    return {"message": "Price Scraper API is running"}


DB_PATH = "data/prices.db"


def get_db():
    return sqlite3.connect(DB_PATH)


@app.get("/prices")
def get_prices(
        shop: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        limit: int = Query(10, le=100),
        offset: int = 0,
        sort_by: str = "timestamp",
        order: str = "desc"
):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT shop, price, timestamp FROM prices WHERE 1=1"
    params = []

    # Фильтры
    if shop:
        query += " AND shop = ?"
        params.append(shop)

    if min_price:
        query += " AND price >= ?"
        params.append(min_price)

    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    # Проверка сортировки
    if sort_by not in ["price", "timestamp"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    query += f" ORDER BY {sort_by} {order}"
    query += " LIMIT ? OFFSET ?"

    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    return [
        {"shop": r[0], "price": r[1], "timestamp": r[2]}
        for r in rows
    ]
