import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3

DB_PATH = "data/prices.db"


def run_analysis():
    conn = sqlite3.connect(DB_PATH)

    # Загружаем данные из БД
    df = pd.read_sql_query(
        "SELECT shop, price, timestamp FROM prices",
        conn
    )

    conn.close()

    # Приводим timestamp к datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Агрегация
    summary = df.groupby("shop")["price"].agg(
        avg_price="mean",
        min_price="min",
        max_price="max"
    ).reset_index()

    # Сохраняем
    summary.to_csv("data/processed/analysis.csv", index=False)

    # График
    for shop in df["shop"].unique():
        subset = df[df["shop"] == shop]
        plt.plot(subset["timestamp"], subset["price"], label=shop)

    plt.legend()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter('%d.%m.%y %H:%M')
    )
    plt.title("Price dynamics")
    plt.tight_layout()
    plt.savefig("data/processed/plot.png")


if __name__ == "__main__":
    run_analysis()
