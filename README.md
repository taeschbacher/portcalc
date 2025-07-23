# portcalc

**portcalc** is a tool for generating a **resampled efficient frontier** to support investors in making **strategic asset allocation** decisions.

The current data collection process is geared towards investors interested primarily in stocks with a base currency of Swiss Francs.

## MSCI Index Data Source

To update the source index data, download the data from [MSCI Index Tools](https://www-cdn.msci.com/web/msci/index-tools/end-of-day-index-data-search).

### Instructions for Downloading Data

Use the following parameters when downloading data via the MSCI web GUI (click on Add/Remove Indexes to add further Countries/Regions):

- **Market: Developed Markets (DM), Scope: Country**:
  - USA
  - Switzerland
  - United Kingdom
  - Japan
- **Market: Developed Markets (DM), Scope: Regional**:
  - EMU (Economic and Monetary Union)
- **Market: Emerging Markets (DM), Scope: Regional**:
  - EM (Emerging Markets)
- **Date Range**: Full History (starting from **December 31, 1969**)
- **Return Type**: Gross
- **Currency**: USD
- **Frequency**: Monthly

Once downloaded, the new data should be appended in "data/historyIndex.csv". The data needs to be appended, because the download date range has been limited and there are now inconsistencies in the time series of the data (new data points seem to be unaffected).

## SNB Exchange Rate Data Source

To update the source index data, download the data from the [SNB data portal](https://data.snb.ch/en).

### Instructions for Downloading Data

Navigate to "Foreign exchange rates" and then to "Foreign exchange rates - Month". Select only "End of month" and download the "CSV (selection)" for the full date range possible.

Once downloaded, the new data should be appended in "data/usdchf.csv".



## ETFs

Selecting and choosing ETFs to implement the strategic asset allocation can be a daunting task, due to the huge selection.

ETF scanners can be of help here:
- [Swissquote](https://www.swissquote.ch/trading-platform/#scanner)
- [justETF](https://www.justetf.com/en/search.html?search=ETFS)

As a general guideline, I like to choose ETFs that have as their benchmark the respective MSCI benchmark or are closely correlated to it (i.e. major stock market index of that country/region, e.g. S&P500 for the USA).

Furthermore, I personally prefer distributing (not accumulating) ETFs and SIX Swiss Exchange listings in Swiss Francs.

Lastly, one should choose the ETF that has a large market capitalization and a cheap TER (total expense ratio).

### My personal (opinionated) ETF list

**USA**:
  - [IE00B3XXRP09](https://www.justetf.com/en/etf-profile.html?isin=IE00B3XXRP09)
**Switzerland**:
  - [CH0237935652](https://www.justetf.com/en/etf-profile.html?isin=CH0237935652)
  - [CH0237935637](https://www.justetf.com/en/etf-profile.html?isin=CH0237935637)
**United Kingdom**:
  - [IE0005042456](https://www.justetf.com/en/etf-profile.html?isin=IE0005042456)
**Japan**:
  - [IE00B95PGT31](https://www.justetf.com/en/etf-profile.html?isin=IE00B95PGT31)
**EMU (Economic and Monetary Union)**:
  - [LU0147308422](https://www.justetf.com/en/etf-profile.html?isin=LU0147308422)
**EM (Emerging Markets)**:
  - [IE00B3VVMM84](https://www.justetf.com/en/etf-profile.html?isin=IE00B3VVMM84)