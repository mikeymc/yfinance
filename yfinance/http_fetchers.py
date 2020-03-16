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