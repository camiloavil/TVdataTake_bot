import requests, json, warnings
from datetime import datetime, timedelta
import time

__version__ = "3.2.10"

class data_TradingV:
    scan_url = "https://scanner.tradingview.com/"
    def __init__(self, cryptosymbol, timeout=None):
        self.cryptosymbol=cryptosymbol
        self.timeout = timeout

    def get_indicators(self,intervals=["1m"],indicators=["close"]):
        if(isinstance(indicators,list)==False):
            return None
        if(isinstance(intervals,list)==False):
            return None
        data = data_TradingV.data(self.cryptosymbol, intervals, indicators)
        #print(json.dumps(data, indent=4))
        #print(json.dumps(data))
        scan_url = f"{data_TradingV.scan_url}crypto/scan"
        headers = {"User-Agent": "tradingview_ta/{}".format(__version__)}
        
        try:
            response = requests.post(scan_url,json=data, headers=headers, timeout=self.timeout)
        except requests.exceptions.ConnectionError as e:
            print(str(datetime.now())+" Error:\n"+str(e))
            return False

        if response.status_code != 200:
            raise Exception("Can't access TradingView's API. HTTP status code: {}. Check for invalid symbol, exchange, or indicators.".format(response.status_code))
        xnow = datetime.now()
        result = json.loads(response.text)["data"]
        #print(result)

        j_result = {}
        #for n_crypto in range(len(self.cryptosymbol)):
        for n_crypto in range(len(result)):
            nivel_I={}
            n_indi_res=0
            for interval in intervals:
                indicators_val = {}
                for n_indi in range(len(indicators)):
                    indicators_val[indicators[n_indi].replace('.','')] = result[n_crypto]["d"][n_indi_res]
                    n_indi_res=n_indi_res+1
                nivel_I[interval]=indicators_val
            j_result[result[n_crypto]["s"]] = nivel_I
        
        j_result["timestamp"]=xnow.timestamp()
        return j_result

    def print_dataPOST(self,interval="1m",indicators=["close"]):
        print(data_TradingV.data(self.cryptosymbol, interval, indicators))

    def print_POST(self,interval="1m",indicators=["close"]):
        data = data_TradingV.data(self.cryptosymbol, interval, indicators)
        scan_url = f"{data_TradingV.scan_url}crypto/scan"
        headers = {"User-Agent": "tradingview_ta/{}".format(__version__)}
        reque = requests.Request('POST',scan_url,json=data, headers=headers)
        req = reque.prepare()
        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

    def data(symbols, intervals, indicators):
        columns=[]
        for interval in intervals:
            temp_alias=data_TradingV.get_alias(interval)
            #print(interval+" - "+temp_alias)
            for indicator in indicators:
                columns.append(indicator+temp_alias)

        #print(columns)
        data_json = {"symbols":{"tickers":[symbol.upper() for symbol in symbols],"query":{"types":[]}},"columns":columns}
        return data_json

    def get_alias(interval):
        if interval == "1m":
            # 1 Minute
            return "|1"
        elif interval == "5m":
            # 5 Minutes
            return "|5"
        elif interval == "15m":
            # 15 Minutes
            return "|15"
        elif interval == "30m":
            # 30 Minutes
            return "|30"
        elif interval == "1h":
            # 1 Hour
            return "|60"
        elif interval == "2h":
            # 2 Hours
            return "|120"
        elif interval == "4h":
            # 4 Hour
            return "|240"
        elif interval == "1W":
            # 1 Week
            return "|1W"
        elif interval == "1M":
            # 1 Month
            return "|1M"
        else:
            if interval != '1d':
                warnings.warn("Interval is empty or not valid, defaulting to 1 day.")
            # Default, 1 Day
            return ""

if __name__ == '__main__':
    #ind= list (["close","open","high","low","volume","BB.upper","BB.lower","RSI7","RSI","RSI[1]","EMA50","EMA100","EMA200","MACD.macd","MACD.signal"])
    ind= list (["close","open","volume"])
    #ind= list (["close","open","high","low","volume","BB.upper","BB.lower","RSI7","MACD.macd","MACD.signal"])
    #par=["BINANCE:BTCBUSDPERP"]
    #par=["BINANCE:BTCBUSDPERP", "BINANCE:ETHBUSDPERP"]
    par=["BINANCE:BTCBUSDPERP", "BINANCE:ETHBUSDPERP", "BINANCE:BNBBUSDPERP" , "BINANCE:SOLBUSDPERP"]
    crypto_data=data_TradingV(cryptosymbol=par ,timeout=1)
    #resul=crypto_data.get_indicators(intervals=["1m","5m","15m"],indicators=ind)
    #resul=crypto_data.get_indicators(intervals=["1m"],indicators=ind)
    #print("")
    #print(json.dumps(resul))
    
    while True:
        resul=crypto_data.get_indicators(intervals=["1m","5m","15m","30m","1h","2h","4h"],indicators=ind)
        dateTaken=datetime.fromtimestamp(resul['timestamp'])
        timebefore=datetime.now().timestamp()
        timeafter=datetime.now().timestamp()
        print(dateTaken.strftime('%H:%M %S.%f')+" "+str(resul),end="\n")
        print("")
        #print("Open1m:"+str(resul["BINANCE:BTCBUSDPERP"]['1m']['open']),end="\t")
        #print("Close1m:"+str(resul["BINANCE:BTCBUSDPERP"]['1m']['close']),end="\t")
        #print("Volume1m:"+str(resul["BINANCE:BTCBUSDPERP"]['1m']['volume']),end="\t")
        #print("Open5m:"+str(resul["BINANCE:BTCBUSDPERP"]['5m']['open']),end="\t")
        #print("Close5m:"+str(resul["BINANCE:BTCBUSDPERP"]['5m']['close']),end="\t")
        #print("Volume5m:"+str(resul["BINANCE:BTCBUSDPERP"]['5m']['volume']),end="\t\t")
        #print("Tb"+datetime.fromtimestamp(timebefore).strftime('%H:%M:%S.%f')+"   Ta:"+datetime.fromtimestamp(timeafter).strftime('%H:%M:%S.%f')+"   diff:"+str(timeafter-timebefore))
        #print("")
        time.sleep(1)

    #.strftime('%S.%f' )
    #xnow=datetime.fromtimestamp(jdata[par]["dataTaken"])

    #crypto_data.print_dataPOST(interval="1h",indicators=ind)
    #crypto_data.print_POST(interval="1m",indicators=ind)
    #par = TA_Handler(symbol="BTCUSDT",screener="crypto",exchange="COINBASE",interval="1h")
    #print(par.get_indicators(ind))

    #https://github.com/shner-elmo/TradingView-Scanner/blob/master/tv_scanner.py

#https://github.com/Mathieu2301/Tradingview-API
#https://github.com/maxoja/tradingview-csv-export-processing

"""[
  "name",
  "change",
  "close",
  "change_abs",
  "high",
  "low",
  "volume",
  "Recommend.All",
  "exchange",
  "High.1M",
  "Low.1M",
  "Pivot.M.Camarilla.Middle",
  "Pivot.M.Camarilla.R1",
  "Pivot.M.Camarilla.R2",
  "Pivot.M.Camarilla.R3",
  "Pivot.M.Camarilla.S1",
  "Pivot.M.Camarilla.S2",
  "Pivot.M.Camarilla.S3",
  "Pivot.M.Classic.Middle",
  "Pivot.M.Classic.R1",
  "Pivot.M.Classic.R2",
  "Pivot.M.Classic.R3",
  "Pivot.M.Classic.S1",
  "Pivot.M.Classic.S2",
  "Pivot.M.Classic.S3",
  "Pivot.M.Demark.Middle",
  "Pivot.M.Demark.R1",
  "Pivot.M.Demark.S1",
  "Pivot.M.Fibonacci.Middle",
  "Pivot.M.Fibonacci.R1",
  "Pivot.M.Fibonacci.R2",
  "Pivot.M.Fibonacci.R3",
  "Pivot.M.Fibonacci.S1",
  "Pivot.M.Fibonacci.S2",
  "Pivot.M.Fibonacci.S3",
  "Pivot.M.Woodie.Middle",
  "Pivot.M.Woodie.R1",
  "Pivot.M.Woodie.R2",
  "Pivot.M.Woodie.R3",
  "Pivot.M.Woodie.S1",
  "Pivot.M.Woodie.S2",
  "Pivot.M.Woodie.S3",
  "High.3M",
  "Low.3M",
  "Perf.3M",
  "price_52_week_high",
  "price_52_week_low",
  "High.6M",
  "Low.6M",
  "Perf.6M",
  "High.All",
  "Low.All",
  "Aroon.Down",
  "Aroon.Up",
  "ADR",
  "ADX",
  "ATR",
  "average_volume_10d_calc",
  "Perf.Y",
  "Perf.YTD",
  "W.R",
  "average_volume_30d_calc",
  "average_volume_60d_calc",
  "average_volume_90d_calc",
  "AO",
  "BB.lower",
  "BB.upper",
  "BBPower",
  "change_abs|15",
  "change|15",
  "change_abs|60",
  "change|60",
  "change_abs|1",
  "change|1",
  "change_abs|240",
  "change|240",
  "change_abs|5",
  "change|5",
  "change_from_open_abs",
  "change_from_open",
  "CCI20",
  "DonchCh20.Lower",
  "DonchCh20.Upper",
  "EMA10",
  "EMA100",
  "EMA20",
  "EMA200",
  "EMA30",
  "EMA5",
  "EMA50",
  "gap",
  "HullMA9",
  "Ichimoku.BLine",
  "Ichimoku.CLine",
  "Ichimoku.Lead1",
  "Ichimoku.Lead2",
  "KltChnl.lower",
  "KltChnl.upper",
  "MACD.macd",
  "MACD.signal",
  "market_cap_calc",
  "Mom",
  "Perf.1M",
  "Recommend.MA",
  "open",
  "Recommend.Other",
  "P.SAR",
  "name",
  "ROC",
  "RSI",
  "RSI7",
  "relative_volume_10d_calc",
  "SMA10",
  "SMA100",
  "SMA20",
  "SMA200",
  "SMA30",
  "SMA5",
  "SMA50",
  "Stoch.D",
  "Stoch.K",
  "Stoch.RSI.K",
  "Stoch.RSI.D",
  "UO",
  "Volatility.D",
  "Volatility.M",
  "Volatility.W",
  "VWAP",
  "VWMA",
  "Perf.W",
  "description",
  "name",
  "type",
  "subtype",
  "update_mode",
  "pricescale",
  "minmov",
  "fractional",
  "minmove2",
  "ADX-DI[1]",
  "Rec.WR",
  "AO",
  "AO[1]",
  "close",
  "BB.lower",
  "BB.upper",
  "Rec.BBPower",
  "CCI20",
  "CCI20[1]",
  "EMA10",
  "EMA100",
  "EMA20",
  "EMA200",
  "EMA30",
  "EMA5",
  "EMA50",
  "Rec.HullMA9",
  "Rec.Ichimoku",
  "MACD.macd",
  "MACD.signal",
  "Mom",
  "Mom[1]",
  "P.SAR",
  "open",
  "Candle.AbandonedBaby.Bearish",
  "Candle.AbandonedBaby.Bullish",
  "Candle.Engulfing.Bearish",
  "Candle.Harami.Bearish",
  "Candle.Engulfing.Bullish",
  "Candle.Harami.Bullish",
  "Candle.Doji",
  "Candle.Doji.Dragonfly",
  "Candle.EveningStar",
  "Candle.Doji.Gravestone",
  "Candle.Hammer",
  "Candle.HangingMan",
  "Candle.InvertedHammer",
  "Candle.Kicking.Bearish",
  "Candle.Kicking.Bullish",
  "Candle.LongShadow.Lower",
  "Candle.LongShadow.Upper",
  "Candle.Marubozu.Black",
  "Candle.Marubozu.White",
  "Candle.MorningStar",
  "Candle.ShootingStar",
  "Candle.SpinningTop.Black",
  "Candle.SpinningTop.White",
  "Candle.3BlackCrows",
  "Candle.3WhiteSoldiers",
  "Candle.TriStar.Bearish",
  "Candle.TriStar.Bullish",
  "RSI",
  "RSI[1]",
  "RSI7",
  "RSI7[1]",
  "SMA10",
  "SMA100",
  "SMA20",
  "SMA200",
  "SMA30",
  "SMA5",
  "SMA50",
  "Stoch.K",
  "Stoch.D",
  "Stoch.K[1]",
  "Stoch.D[1]",
  "Rec.Stoch.RSI",
  "Rec.UO",
  "Rec.VWMA",
["""