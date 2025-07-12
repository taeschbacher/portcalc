import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from utils.portfolio_functions import portfolio_return


def save_plots(
    data, result_resampled, result_efficient_frontier, max_sr_portfolio, portfolios
):
    save_plot_index(data=data, index_name="ch")
    save_plot_area(data=data, result_resampled=result_resampled, portfolios=portfolios)
    save_plot_efficient_frontier(result_efficient_frontier)
    save_plot_index_max_sr_portfolio(data, result_resampled, max_sr_portfolio)


def save_plot_index(data, index_name):
    plt.figure()
    fig, ax = plt.subplots(constrained_layout=True)
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.ylabel("Total return index")
    ax.plot(
        pd.to_datetime(data.index, format="%Y-%m-%d"),
        (data[index_name].to_numpy() + 1).cumprod() * 100,
    )
    plt.savefig(f"plots/index_{index_name}.pdf", format="pdf")


def save_plot_index_max_sr_portfolio(data, result_resampled, max_sr_portfolio):
    plt.figure()
    fig, ax = plt.subplots(constrained_layout=True)
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    plt.ylabel("Total return index")
    ax.plot(
        pd.to_datetime(data.index, format="%Y-%m-%d"),
        (
            portfolio_return(
                return_np=data.to_numpy(),
                weight_np=result_resampled[:, max_sr_portfolio],
            )
            + 1
        ).cumprod()
        * 100,
    )
    plt.savefig("plots/index_max_sr_portfolio.pdf", format="pdf")


def save_plot_area(data, result_resampled, portfolios):
    plt.figure()
    plt.stackplot(range(portfolios), result_resampled, labels=data.T.index)
    plt.legend(loc="lower left")
    plt.ylabel("Portfolio allocation")
    plt.xlabel("Portfolio")
    plt.savefig("plots/area.pdf", format="pdf")


def save_plot_efficient_frontier(result_efficient_frontier):
    plt.figure()
    plt.plot(result_efficient_frontier[0, :], result_efficient_frontier[1, :])
    plt.ylabel("Return")
    plt.xlabel("Volatility")
    plt.savefig("plots/efficient_frontier.pdf", format="pdf")
