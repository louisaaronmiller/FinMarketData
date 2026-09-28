# FinMarketData

# Market Data Analysis – VWAP

A Python project for analysing market trade data and calculating **Volume Weighted Average Price (VWAP)** across different stocks, dates, and exchanges.

The project is built with **Python and pandas**, with an emphasis on making the analysis reusable rather than hard-coding it for a particular pair of exchanges.

## Project Overview

The main task is to take trade-level market data and calculate the VWAP for each stock on a given exchange.

VWAP is calculated as:

\[
VWAP = \frac{\sum (Price \times Volume)}{\sum Volume}
\]

For each stock, the project therefore:

1. Filters the data by date and exchange.
2. Calculates the value of each trade (`price × size`).
3. Groups trades by stock.
4. Sums the traded volume and traded value.
5. Calculates the VWAP.
6. Allows VWAPs from multiple exchanges to be compared.

The project also includes functionality for generating additional test data.

## Main Features

- Calculate VWAP for a selected date and exchange.
- Calculate VWAPs for multiple exchanges.
- Compare VWAPs between exchanges.
- Identify which exchange has the highest VWAP for each stock.
- Calculate the absolute VWAP difference when comparing two exchanges.
- Sort stocks by VWAP difference.
- Filter results to stocks where a particular exchange has the highest VWAP.
- Validate user-selected exchanges and invalid date/exchange combinations.
- Generate additional random market data for testing.
- Designed so that the comparison is not restricted to a hard-coded `N` vs `O` exchange pair.

## Data

The project reads market data from:

```text
data/sampleData.csv
```

The expected columns are:

| Column | Description |
|---|---|
| `date` | Trading date |
| `time` | Time of the trade |
| `stock` | Stock ticker |
| `price` | Price of the trade |
| `size` | Trade size / volume |
| `exchange` | Exchange on which the trade occurred |

The example data uses `N` for NYSE and `O` for NASDAQ, although the analysis functions can work with other exchange identifiers present in the dataset.

However, data can be generated using the `generateData()` function.

## Functions

### `calculateVWAP()`

```python
calculateVWAP(date, exchange, dataframe)
```

Calculates the VWAP for every stock on a particular date and exchange.

The function first filters the dataframe:

```python
df = dataframe[
    (dataframe["exchange"] == exchange) &
    (dataframe["date"] == date)
].copy()
```

A copy is used so that new columns can be added to the filtered dataframe without modifying the original dataframe.

The trade value is then calculated:

```python
df["total"] = df["price"] * df["size"]
```

The data is grouped by date and stock, and both volume and total traded value are summed:

```python
group = df.groupby(["date", "stock"])[["size", "total"]].sum()
```

Finally:

```python
group["vwap"] = group["total"] / group["size"]
```

The function returns a pandas `Series` containing the VWAP for each stock.

### `exchangeDict()`

```python
exchangeDict(date, dataframe, selected_exchanges=None)
```

Calculates VWAPs for multiple exchanges and stores the results in a dictionary.

The dictionary structure is:

```python
{
    "N": <VWAP Series>,
    "O": <VWAP Series>
}
```

An optional `selected_exchanges` argument allows the caller to choose which exchanges should be included.

For example:

```python
exchangeDict(
    "2021-10-01",
    df,
    selected_exchanges=["N", "K"]
)
```

This means the comparison logic does not need to assume that the user is always comparing NYSE and NASDAQ.

The function also checks that requested exchanges actually exist in the dataset and raises a `ValueError` if they do not.

### `highestVWAP()`

```python
highestVWAP(dataSeries, exchange_prio=None, sort_by_difference=False)
```

Compares the VWAP Series returned by `exchangeDict()`.

The dictionary is combined into a DataFrame using:

```python
df = pd.concat(dataSeries, axis=1)
```

Because the dictionary keys are used as the column names, the resulting DataFrame has one VWAP column per exchange.

For example:

```text
        N       K
AAPL    150.2   149.8
AMD     120.4   121.1
NVDA    450.1   448.9
```

The highest VWAP for each stock is then found using:

```python
max_vwap = df.max(axis=1)
max_exchange = df.idxmax(axis=1)
```

The final result contains:

- the highest VWAP
- the exchange providing that VWAP
- the VWAP difference when exactly two exchanges are being compared

Example output structure:

```text
          vwap exchange  difference
AAPL     150.2       N        0.4
AMD      121.1       K        0.7
NVDA     450.1       N        1.2
```

#### Exchange priority

The optional `exchange_prio` argument can be used to return only stocks where a particular exchange has the highest VWAP.

For example:

```python
highestVWAP(
    exchange_dict,
    exchange_prio="N"
)
```

This is useful when the analysis needs to identify stocks for which a particular exchange has the higher VWAP.

#### Sorting by difference

When exactly two exchanges are being compared, the optional:

```python
sort_by_difference=True
```

sorts the results from the largest VWAP difference to the smallest.

## Test Data Generation

### `generateData()`

```python
generateData(dataframe, exchanges, pricestart, priceend)
```

This function generates additional random trades for testing.

The generated records include:

- date
- time
- stock
- price
- trade size
- exchange

For example:

```python
df2 = generateData(df, ["N", "K"], 45, 47)
```

This creates additional NVDA trades with prices randomly generated between 45 and 47 and randomly assigns them to the selected exchanges.

The generated rows are then appended to the existing dataset using `pd.concat()`.

This was useful for testing the analysis with different exchange combinations and additional market data without manually creating a large dataset.

## Error Handling

The project includes validation for invalid inputs.

If an exchange or date does not produce any data:

```python
ValueError("Incorrect Date or Exchange")
```

is raised by `calculateVWAP()`.

`exchangeDict()` also validates explicitly selected exchanges before attempting the calculation:

```python
ValueError(
    f"exchange: {i} in selected_exchanges was not found in data"
)
```

If `highestVWAP()` is asked to prioritise an exchange which does not have the highest VWAP for any stock, it raises an error rather than returning an empty result.

## Design Choices

### Reusable exchange selection

Rather than assuming that the comparison is always between two specific exchanges, the project accepts an exchange list:

```python
selected_exchanges=["N", "K"]
```

This makes the analysis more reusable if the dataset contains additional exchanges.

### Pandas groupby

`groupby()` is used to aggregate individual trades into stock-level statistics.

This avoids manually looping through every trade and allows pandas to perform the aggregation efficiently.

### Pandas Series and DataFrames

`calculateVWAP()` returns a `Series` because the result is a single VWAP value per stock.

`highestVWAP()` produces a `DataFrame` because the comparison contains multiple pieces of information for each stock:

- VWAP
- exchange
- difference

### Concatenating exchange results

`pd.concat()` is used to combine the individual exchange Series side-by-side.

Using the exchange names as dictionary keys means the exchange identity is preserved automatically as the resulting DataFrame's column names.

## Technologies

- **Python**
- **pandas**
- Python `datetime`
- Python `random`

## Running the Project

Install pandas if necessary:

```bash
pip install pandas
```

Then run:

```bash
python MarketAnalysis.py
```

Make sure the working directory allows the program to locate:

```text
data/sampleData.csv
```

## Project Structure

A simple project structure is:

```text
FinMarketData/
├── MarketAnalysis.py
├── data/
│   └── sampleData.csv
└── README.md
```

## Notes

This project was designed around an extensible market-data analysis workflow. The functions are separated by responsibility: calculating VWAP, organising results by exchange, comparing those results, and generating test data. This makes individual parts of the analysis easier to test and extend independently.
