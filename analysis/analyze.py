import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def run_analysis():
    df = pd.read_csv("data/raw/prices.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    summary = df.groupby("shop")["price"].agg(
        avg_price="mean",
        min_price="min",
        max_price="max"
    ).reset_index()

    summary.to_csv("data/processed/analysis.csv", index=False)

    for shop in df["shop"].unique():
        subset = df[df["shop"] == shop]
        plt.plot(subset["timestamp"], subset["price"], label=shop)

    plt.legend()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))
    plt.title("Price dynamics")
    plt.tight_layout()
    plt.savefig("data/processed/plot.png")


if __name__ == "__main__":
    run_analysis()
