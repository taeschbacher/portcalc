import numpy as np
import pandas as pd
import random
import quadprog

from utils.portfolio_functions import portfolio_return


def get_max_sr_portfolio(result_efficient_frontier, portfolios):
    result_sr_portfolio = np.zeros(portfolios)

    for x in range(portfolios):
        result_sr_portfolio[x] = (
            result_efficient_frontier[1, x] / result_efficient_frontier[0, x]
        )

    max_sr_portfolio = np.where(result_sr_portfolio == result_sr_portfolio.max())[0][0]

    return max_sr_portfolio


def get_efficient_frontier(data, result_resampled, portfolios):
    result_efficient_frontier = np.zeros((2, portfolios))

    for x in range(portfolios):
        result_efficient_frontier[0, x] = np.std(
            portfolio_return(
                return_np=data.to_numpy(), weight_np=result_resampled[:, x]
            )
        ) * np.sqrt(12)
        result_efficient_frontier[1, x] = (
            np.mean(
                portfolio_return(
                    return_np=data.to_numpy(), weight_np=result_resampled[:, x]
                )
            )
            * 12
        )

    return result_efficient_frontier


def data_preparation():
    usdchf = pd.read_csv("data/usdchf.csv", delimiter=";", index_col="Date")
    usdchf = usdchf.query('D1 == "USD1" and D0 == "M1"')

    usdchf["return"] = usdchf["Value"] / usdchf["Value"].shift(1) - 1

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

    historyIndex["usa_return"] = historyIndex["usa"] / historyIndex["usa"].shift(1) - 1
    historyIndex["ch_return"] = historyIndex["ch"] / historyIndex["ch"].shift(1) - 1
    historyIndex["uk_return"] = historyIndex["uk"] / historyIndex["uk"].shift(1) - 1
    historyIndex["jp_return"] = historyIndex["jp"] / historyIndex["jp"].shift(1) - 1
    historyIndex["emu_return"] = historyIndex["emu"] / historyIndex["emu"].shift(1) - 1
    historyIndex["em_return"] = historyIndex["em"] / historyIndex["em"].shift(1) - 1

    merged = pd.merge(
        historyIndex, usdchf, how="left", on="month", suffixes=("_index", "_usdchf")
    )

    merged["usa_return_chf"] = merged["usa_return"] + merged["return"]
    merged["ch_return_chf"] = merged["ch_return"] + merged["return"]
    merged["uk_return_chf"] = merged["uk_return"] + merged["return"]
    merged["jp_return_chf"] = merged["jp_return"] + merged["return"]
    merged["emu_return_chf"] = merged["emu_return"] + merged["return"]
    merged["em_return_chf"] = merged["em_return"] + merged["return"]

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


def simulation(data, portfolios, simulations):
    assets = data.shape[1]

    result = np.zeros((simulations, assets, portfolios))
    result_resampled = np.zeros((assets, portfolios))
    result_efficient_frontier = np.zeros((2, portfolios))

    result_meta = np.zeros((simulations, assets, portfolios))
    result_resampled_meta = np.zeros((assets, portfolios))

    for r in range(simulations):
        dat_meta = data.loc[
            data.index[random.choices(range(0, data.shape[0]), k=data.shape[0])]
        ]

        for s in range(simulations):
            dat = dat_meta.loc[
                dat_meta.index[
                    random.choices(range(0, dat_meta.shape[0]), k=dat_meta.shape[0])
                ]
            ].to_numpy()

            increment = (np.mean(dat, axis=0).max() - np.mean(dat, axis=0).min()) / (
                portfolios + 1
            )
            target_return = np.mean(dat, axis=0).min()
            for x in range(portfolios):
                target_return = target_return + increment

                C1 = np.column_stack(
                    (np.ones(assets, dtype=float), np.mean(dat, axis=0, dtype=float))
                )
                C2 = np.concatenate(
                    (np.eye(assets, dtype=float), np.eye(assets, dtype=float) * -1),
                    axis=1,
                )
                C = np.concatenate((C1, C2), axis=1)

                b1 = np.array([1, target_return], dtype=float)
                b2 = np.concatenate(
                    (np.zeros(assets, dtype=float), np.ones(assets, dtype=float) * -1)
                )
                b = np.concatenate((b1, b2))

                try:
                    result[s, :, x] = quadprog.solve_qp(
                        G=np.cov(dat.T),
                        a=np.zeros(assets, dtype=float),
                        C=C,
                        b=b,
                        meq=2,
                    )[0]
                except Exception:
                    pass

            for x in range(portfolios):
                result_efficient_frontier[0, x] = np.std(
                    portfolio_return(return_np=dat, weight_np=result[s, :, x])
                )
                result_efficient_frontier[1, x] = np.mean(
                    portfolio_return(return_np=dat, weight_np=result[s, :, x])
                )

            minimum_variance_portfolio = np.where(
                result_efficient_frontier[0, :] == result_efficient_frontier[0, :].min()
            )[0][0]
            minimum_variance_return = result_efficient_frontier[
                1, minimum_variance_portfolio
            ]

            increment = (np.mean(dat, axis=0).max() - minimum_variance_return) / (
                portfolios + 1
            )
            target_return = minimum_variance_return
            for x in range(portfolios):
                target_return = target_return + increment

                C1 = np.column_stack(
                    (np.ones(assets, dtype=float), np.mean(dat, axis=0, dtype=float))
                )
                C2 = np.concatenate(
                    (np.eye(assets, dtype=float), np.eye(assets, dtype=float) * -1),
                    axis=1,
                )
                C = np.concatenate((C1, C2), axis=1)

                b1 = np.array([1, target_return], dtype=float)
                b2 = np.concatenate(
                    (np.zeros(assets, dtype=float), np.ones(assets, dtype=float) * -1)
                )
                b = np.concatenate((b1, b2))

                try:
                    result[s, :, x] = quadprog.solve_qp(
                        G=np.cov(dat.T),
                        a=np.zeros(assets, dtype=float),
                        C=C,
                        b=b,
                        meq=2,
                    )[0]
                except Exception:
                    pass

        for y in range(portfolios):
            for x in range(assets):
                result_resampled[x, y] = (result[:, x, y]).mean()

        for y in range(portfolios):
            for x in range(assets):
                result_meta[r, x, y] = result_resampled[x, y]

        if (r + 1) % 10 == 0:
            print("Simulation " + str(r + 1) + " of " + str(simulations))

    for y in range(portfolios):
        for x in range(assets):
            result_resampled_meta[x, y] = (result_meta[:, x, y]).mean()

    return result_resampled_meta
