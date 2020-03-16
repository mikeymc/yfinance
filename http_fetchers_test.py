import unittest
import yfinance as yf


class TestEndpointsResponseCodes(unittest.TestCase):
    def test_business_insider(self):
        response = yf.HttpFetcher.fetch_from_business_insider('Brighthouse Financial, Inc. - 6')
        self.assertRegex(response, r'Stocks')
        self.assertRegex(response, r'Indices')


if __name__ == '__main__':
    unittest.main()
