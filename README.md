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
