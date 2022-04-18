import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import ssl


class YHFinanceService:
    base_url: str = "https://yh-finance.p.rapidapi.com"
    api_key: str

    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_financials(self, symbol):
        request = Request(self.base_url + f"/stock/v2/get-financials?symbol={symbol}")
        request.add_header("x-rapidapi-key", self.api_key)
        try:
            response = urlopen(request, context=ssl.SSLContext())
        except HTTPError:
            return None
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))
        return json_data


def getprice(symbol, api_key):
    service = YHFinanceService(api_key)
    data = service.get_stock_financials(symbol)
    if data is None:
        raise ValueError("could not get data from API")
    regular_market_open_value = data["price"]["regularMarketOpen"]["raw"]
    return regular_market_open_value


g_exportedScripts = (getprice,)
