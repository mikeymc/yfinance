import unittest
import yfinance as yf


class TestEndpointsResponseCodes(unittest.TestCase):
    def test_business_insider(self):
        response = yf.HttpFetcher.fetch_from_business_insider('Brighthouse Financial, Inc. - 6')
        self.assertRegex(response, r'Stocks')
        self.assertRegex(response, r'Indices')

    def test_yahoo_finance_v8_fetcher(self):
        response = yf.HttpFetcher.fetch_from_yahoo_finance_v8('MSFT')
        self.assertEquals(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data['chart'])
        self.assertIsNotNone(data['chart']['result'])
        self.assertIsNotNone(data['chart']['result'][0])
        self.assertIsNotNone(data['chart']['result'][0]['timestamp'])
        self.assertIsNotNone(data['chart']['result'][0]['indicators'])


if __name__ == '__main__':
    unittest.main()
