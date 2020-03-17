#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yahoo! Finance market data downloader (+fix for Pandas Datareader)
# https://github.com/ranaroussi/yfinance
#
# Copyright 2017-2019 Ran Aroussi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import datetime as _datetime
import requests as _requests
import pandas as _pd
import json
from .base import TickerBase


class Ticker(TickerBase):

    def __repr__(self):
        return 'yfinance.Ticker object <%s>' % self.ticker

    def _download_options(self, date=None, proxy=None):
        url = "{}/v7/finance/options/{}?date={}".format(self._base_url, self.ticker, date)

        # setup proxy in requests format
        if proxy is not None:
            if isinstance(proxy, dict) and "https" in proxy:
                proxy = proxy["https"]
            proxy = {"https": proxy}

        r = _requests.get(url=url, proxies=proxy).json()
        try:
            for exp in r['optionChain']['result'][0]['expirationDates']:
                self._expirations[_datetime.datetime.fromtimestamp(
                    exp).strftime('%Y-%m-%d')] = exp
            return r['optionChain']['result'][0]['options'][0]
        except:
            return {}

    def _options2df(self, opt, tz=None):
        data = _pd.DataFrame(opt).reindex(columns=[
            'contractSymbol',
            'lastTradeDate',
            'strike',
            'lastPrice',
            'bid',
            'ask',
            'change',
            'percentChange',
            'volume',
            'openInterest',
            'impliedVolatility',
            'inTheMoney',
            'contractSize',
            'currency'])

        data['lastTradeDate'] = _pd.to_datetime(
            data['lastTradeDate'], unit='s')
        if tz is not None:
            data['lastTradeDate'] = data['lastTradeDate'].tz_localize(tz)
        return data

    def to_json(self):
        return json.dumps(self, cls=TickerEncoder)

    def to_dict(self):
        def de_timestamp(obj):
            for k, v in obj.items():
                if isinstance(k, _pd.Timestamp):
                    return k.ctime()

        dividends = self.dividends.to_dict()
        recommendations = self.recommendations
        recommendations.reset_index(drop=True, inplace=True)
        return_object = {
            'isin': self.isin,
            'info': self.info,
            'majority_holders': de_timestamp(self.major_holders.to_dict()),
            'institutional_holders': de_timestamp(self.institutional_holders.to_dict()),
            'dividends': de_timestamp(dividends),
            'splits': de_timestamp(self.splits.to_dict()),
            'actions': de_timestamp(self.actions.to_dict()),
            'calendar': de_timestamp(self.calendar.to_dict()),
            'recommendations': de_timestamp(recommendations.to_dict()),
            'earnings': de_timestamp(self.earnings.to_dict()),
            'quarterly_earnings': de_timestamp(self.quarterly_earnings.to_dict()),
            'financials': de_timestamp(self.financials.to_dict()),
            'quarterly_financials': de_timestamp(self.quarterly_financials.to_dict()),
            'balance_sheet': de_timestamp(self.balance_sheet.to_dict()),
            'quarterly_balance_sheet': de_timestamp(self.quarterly_balance_sheet.to_dict()),
            'cashflow': de_timestamp(self.cashflow.to_dict()),
            'quarterly_cashflow': de_timestamp(self.quarterly_cashflow.to_dict()),
            'sustainability': de_timestamp(self.sustainability.to_dict()) if self.sustainability is not None else None,
            'options': list(self.options)
        }
        return return_object

    # ------------------------

    @property
    def isin(self):
        return self.get_isin()

    @property
    def major_holders(self):
        return self.get_major_holders()

    @property
    def institutional_holders(self):
        return self.get_institutional_holders()

    @property
    def dividends(self):
        return self.get_dividends()

    @property
    def dividends(self):
        return self.get_dividends()

    @property
    def splits(self):
        return self.get_splits()

    @property
    def actions(self):
        return self.get_actions()

    @property
    def info(self):
        return self.get_info()

    @property
    def calendar(self):
        return self.get_calendar()

    @property
    def recommendations(self):
        return self.get_recommendations()

    @property
    def earnings(self):
        return self.get_earnings()

    @property
    def quarterly_earnings(self):
        return self.get_earnings(freq='quarterly')

    @property
    def financials(self):
        return self.get_financials()

    @property
    def quarterly_financials(self):
        return self.get_financials(freq='quarterly')

    @property
    def balance_sheet(self):
        return self.get_balancesheet()

    @property
    def quarterly_balance_sheet(self):
        return self.get_balancesheet(freq='quarterly')

    @property
    def balancesheet(self):
        return self.get_balancesheet()

    @property
    def quarterly_balancesheet(self):
        return self.get_balancesheet(freq='quarterly')

    @property
    def cashflow(self):
        return self.get_cashflow()

    @property
    def quarterly_cashflow(self):
        return self.get_cashflow(freq='quarterly')

    @property
    def sustainability(self):
        return self.get_sustainability()

    @property
    def options(self):
        if not self._expirations:
            self._download_options()
        return tuple(self._expirations.keys())


class TickerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Ticker):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)
