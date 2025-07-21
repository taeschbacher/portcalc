import pandas as pd

from data.data import data_preparation
from portcalc.portcalc import simulation
from portcalc.portcalc import get_efficient_frontier
from portcalc.portcalc import get_max_sr_portfolio
from plots.plots import save_plots


def main():
    portfolios = 50
    simulations = 1000

    data = data_preparation()

    result_resampled_meta = simulation(
        data=data, portfolios=portfolios, simulations=simulations
    )

    result_efficient_frontier = get_efficient_frontier(
        data=data, result_resampled=result_resampled_meta, portfolios=portfolios
    )

    max_sr_portfolio = get_max_sr_portfolio(
        result_efficient_frontier=result_efficient_frontier, portfolios=portfolios
    )

    save_plots(
        data=data,
        result_resampled=result_resampled_meta,
        result_efficient_frontier=result_efficient_frontier,
        max_sr_portfolio=max_sr_portfolio,
        portfolios=portfolios,
    )

    pd.DataFrame(result_resampled_meta, index=data.T.index).to_csv(
        "results/resampled.csv", sep=";"
    )
    pd.DataFrame(result_efficient_frontier, index=["Volatility", "Return"]).to_csv(
        "results/efficient_frontier.csv", sep=";"
    )
    pd.DataFrame(result_resampled_meta, index=data.T.index)[max_sr_portfolio].to_csv(
        "results/allocation.csv", sep=";", header=False
    )


if __name__ == "__main__":
    main()
