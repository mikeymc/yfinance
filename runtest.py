#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Yahoo! Finance market data downloader (+fix for Pandas Datareader)
# https://github.com/ranaroussi/yfinance

"""
Sanity check for most common library uses all working

- Stock: Microsoft
- ETF: Russell 2000 Growth
- Mutual fund: Vanguard 500 Index fund
- Index: S&P500
- Currency BTC-USD
"""

from __future__ import print_function
import yfinance as yf
import json
from urllib.error import HTTPError
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm


def test_yfinance():
    for symbol in ['MSFT', 'IWO', 'VFINX', '^GSPC', 'BTC-USD']:
        print(">>", symbol, end=' ... ')
        ticker = yf.Ticker(symbol)

        # always should have info and history for valid symbols
        assert(ticker.info is not None and ticker.info != {})
        assert(ticker.history(period="max").empty is False)

        # following should always gracefully handled, no crashes
        ticker.cashflow
        ticker.balance_sheet
        ticker.financials
        ticker.sustainability
        ticker.major_holders
        ticker.institutional_holders

        print("OK")


def test_ticker_to_json():
    print(">>", "to_json()", end=' ... ')
    yf.Ticker('BHFAL').to_json()
    yf.Ticker('ACTTW').to_json()
    yf.Ticker('ADP').to_json()
    yf.Ticker('MSFT').to_json()
    yf.Ticker('ALACR').to_json()
    yf.Ticker('ALYA').to_json()
    yf.Ticker('ACAMW').to_json()
    yf.Ticker('ACTT').to_json()
    print("OK")


def test_big_list_per_ticker():
    def run(t):
        try:
            yf.Ticker(t).to_json()
        except HTTPError:
            pass

    print(">>", "to_json()", end=' ... ')
    tickers = open('source_files/nasdaqlisted.txt').read().split()
    tickers += open('source_files/otherlisted.txt').read().split()
    print(">> Testing", len(tickers), "tickers")
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(run)(t) for t in tqdm(tickers))
    print("OK")


def test_tickers_to_json():
    print(">>", "to_json()", end=' ... ')
    tickers = open('source_files/nasdaqlisted.txt').read().split()
    tickers += open('source_files/otherlisted.txt').read().split()
    ticker_json = yf.Tickers(tickers).to_json()
    json.loads(ticker_json)
    ticker_json = yf.Tickers(tickers).to_json()
    json.loads(ticker_json)
    print("OK")


def test_tickers_download():
    print(">>", "download()", end=' ... ')
    tickers = open('source_files/nasdaqlisted.txt').read().split()
    tickers += open('source_files/otherlisted.txt').read().split()
    json.loads(yf.Tickers(tickers).download().to_json())
    print("OK")


if __name__ == "__main__":
    test_yfinance()
    # test_tickers_to_json()
    test_ticker_to_json()
    # test_big_list_per_ticker()
    # test_tickers_download()
