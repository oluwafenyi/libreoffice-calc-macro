import json
from urllib.request import urlopen, Request
import ssl


class YHFinanceService:
    base_url: str = "https://yh-finance.p.rapidapi.com"
    api_key: str

    def __init__(self, api_key):
        self.api_key = api_key

    def autocomplete(self, query):
        request = Request(self.base_url + f"/auto-complete?q={query}")
        request.add_header("x-rapidapi-key", self.api_key)
        response = urlopen(request, context=ssl.SSLContext())
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))
        return json_data

    def get_stock_financials(self, symbol):
        request = Request(self.base_url + f"/stock/v2/get-financials?symbol={symbol}")
        request.add_header("x-rapidapi-key", self.api_key)
        response = urlopen(request, context=ssl.SSLContext())
        data = response.read()
        json_data = json.loads(data.decode("utf-8"))
        return json_data


def getprice(stock_id, api_key):
    service = YHFinanceService(api_key)
    data = service.autocomplete(stock_id)
    try:
        stock_symbol = data["quotes"][0]["symbol"]
    except Exception:
        raise ValueError("WKN seems to be invalid, could not convert to stock symbol")
    data = service.get_stock_financials(stock_symbol)

    regular_market_open_value = data["price"]["regularMarketOpen"]["raw"]
    return regular_market_open_value


g_exportedScripts = (getprice,)
