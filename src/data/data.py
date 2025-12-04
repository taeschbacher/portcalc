import pandas as pd


def data_preparation():
    usdchf = pd.read_csv("data/usdchf.csv", delimiter=";", index_col="Date")
    usdchf = usdchf.query('D1 == "USD1" and D0 == "M1"')

    historyIndex = pd.read_csv(
        "data/historyIndex.csv", delimiter=";", index_col="Date", thousands=","
    )

    historyIndex = historyIndex.rename(
        columns={
            "USA Standard (Large+Mid Cap)": "usa",
            "SWITZERLAND Standard (Large+Mid Cap)": "ch",
            "UNITED KINGDOM Standard (Large+Mid Cap)": "uk",
            "JAPAN Standard (Large+Mid Cap)": "jp",
            "EMU Standard (Large+Mid Cap)": "emu",
            "EM (EMERGING MARKETS) Standard (Large+Mid Cap)": "em",
        }
    )

    usdchf["date"] = pd.to_datetime(usdchf.index, format="%Y-%m")
    usdchf["month"] = usdchf["date"].dt.to_period("M")

    historyIndex["date"] = pd.to_datetime(historyIndex.index, format="%b %d, %Y")
    historyIndex["month"] = historyIndex["date"].dt.to_period("M")

    merged = pd.merge(
        historyIndex, usdchf, how="left", on="month", suffixes=("_index", "_usdchf")
    )

    merged["usa_return_chf"] = (merged["usa"] * merged["Value"]) / (
        merged["usa"].shift(1) * merged["Value"].shift(1)
    ) - 1
    merged["ch_return_chf"] = (merged["ch"] * merged["Value"]) / (
        merged["ch"].shift(1) * merged["Value"].shift(1)
    ) - 1
    merged["uk_return_chf"] = (merged["uk"] * merged["Value"]) / (
        merged["uk"].shift(1) * merged["Value"].shift(1)
    ) - 1
    merged["jp_return_chf"] = (merged["jp"] * merged["Value"]) / (
        merged["jp"].shift(1) * merged["Value"].shift(1)
    ) - 1
    merged["emu_return_chf"] = (merged["emu"] * merged["Value"]) / (
        merged["emu"].shift(1) * merged["Value"].shift(1)
    ) - 1
    merged["em_return_chf"] = (merged["em"] * merged["Value"]) / (
        merged["em"].shift(1) * merged["Value"].shift(1)
    ) - 1

    returns_chf = merged[
        [
            "date_index",
            "usa_return_chf",
            "ch_return_chf",
            "uk_return_chf",
            "jp_return_chf",
            "emu_return_chf",
            "em_return_chf",
        ]
    ]

    returns_chf = returns_chf.rename(
        columns={
            "date_index": "date",
            "usa_return_chf": "usa",
            "ch_return_chf": "ch",
            "uk_return_chf": "uk",
            "jp_return_chf": "jp",
            "emu_return_chf": "emu",
            "em_return_chf": "em",
        }
    )

    data = returns_chf.set_index("date").dropna()
    data.to_csv("data/returns_chf.csv", sep=";")

    return data
