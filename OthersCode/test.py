import requests
import json

url = "https://scanner.tradingview.com/crypto/scan?"

headers = {
        "cache-control": "no-cache",
        #"x-dreamfactory-api-key": "YOUR_API_KEY"
}
jdata={}
data = {"symbols":{"tickers":["BINANCE:BTCBUSDPERP"],"query":{"types":[]}},"columns":['close','open','Recommend.All']}
#print(json.dumps(data, indent=4))
jsymbols={}
jsymbols['tickers']=['BINANCE:BTCBUSDPERP','BINGX:BTCUSDT']
jsymbols['query']={"types":[]}
jdata['symbols']=jsymbols
jdata['columns']=["close|60", "open|60", "high|60", "low|60", "volume|60","close|30", "open|30", "high|30", "low|30", "volume|240"]

#jtry=json.loads('{"filter":[{"left":"market_cap_basic","operation":"nempty"},{"left":"type","operation":"in_range","right":["stock","dr","fund"]},{"left":"subtype","operation":"in_range","right":["common","","etf","unit","mutual","money","reit","trust"]},{"left":"exchange","operation":"in_range","right":["AMEX","NASDAQ","NYSE"]}],"options":{"lang":"en"},"symbols":{"query":{"types":[]},"tickers":[]},"columns":["name","close","change","change_abs","Recommend.All","volume","market_cap_basic","price_earnings_ttm","earnings_per_share_basic_ttm","number_of_employees","sector","industry","description","name","type","subtype","update_mode","pricescale","minmov","fractional","minmove2"],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"range":[0,5000]}')
#print(json.dumps(jtry,indent=4))
response = requests.post(url,json=jdata, headers=headers, timeout=2)
#response = requests.request("POST", url, headers=headers)

print(response.text)