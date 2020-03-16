import requests as _requests

try:
    from urllib.parse import quote as urlencode
except ImportError:
    from urllib import quote as urlencode


class HttpFetcher:
    def fetch_from_business_insider(query, proxy=None):
        url = 'https://markets.businessinsider.com/ajax/' \
              'SearchController_Suggest?max_results=25&query=%s' \
            % urlencode(query)
        return _requests.get(url=url, proxies=proxy).text

    def fetch_from_yahoo_finance_v8(ticker_symbol, params=None, proxy=None):
        url = "https://query1.finance.yahoo.com/v8/finance/chart/{}".format(ticker_symbol)
        return _requests.get(url=url, params=params, proxies=proxy)
