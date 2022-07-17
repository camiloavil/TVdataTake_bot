from hashlib import new
import sys, signal, json
import time as t
import threading as th
from source.db.db_real import DBReal
from source.config.configP import config
from datetime import datetime, timedelta
from source.takedata.TradingViewData import data_TradingV

class trackingData():
    timer=None
    dataTake=None
    pares=None

    def init():
        trackingData.UpdatePares()
        signal.signal(signal.SIGINT, trackingData.letsexit)
        signal.signal(signal.SIGTERM,trackingData.letsexit)
        DBReal.createTableData()
        #print("Check: "+str(trackingData.pares))
        t.sleep((60-t.time()%60)+0) #sleep to the start of next min
        trackingData.run()

    def UpdatePares():
        config.refresh()
        new_pares=config.getlist('DataTake','data_crypto')
        if(new_pares!=trackingData.pares):
            print("Check: "+str(new_pares))
        trackingData.pares=config.getlist('DataTake','data_crypto')
        trackingData.dataTake=data_TradingV(cryptosymbol=trackingData.pares ,timeout=2)

    def run():
        trackingData.timer=th.Timer(60,trackingData.run)
        trackingData.timer.start()
        trackingData.getData()
    
    def getData():
        intervals=trackingData.getIntervals()
        #print("take "+str(intervals),end="\n")
        validator=trackingData.resetValidator(intervals)
        dataF=trackingData.dataTake.get_indicators(intervals,config.getlist('DataTake','indicators'))
        #print(datetime.fromtimestamp(dataF['timestamp']).strftime('%H:%M %S.%f')+"\tChecking",end="\t")
        while((int(t.time()%60)<config.getint('DataTake','secLimit'))and(trackingData.checkValidator(validator))):
            t.sleep(2)
            dataS=trackingData.dataTake.get_indicators(intervals,config.getlist('DataTake','indicators'))
            if(dataF!=False and dataS != False):
                validator=trackingData.checkDatas(dataF,dataS,validator)
                #print(datetime.fromtimestamp(dataF['timestamp']).strftime('%H:%M %S.%f')+"\tChecking",end="\t")
            if(dataS != False):
                dataF=dataS
        if(trackingData.checkValidator(validator)==True):
            print("Error en Captura "+str(config.getint('DataTake','secLimit'))+"secL "+str(datetime.now()),end="\n")
            print(json.dumps(validator, indent=4))
        #Actulizar lista de pares        
        trackingData.UpdatePares()

    def checkDatas(first,second,validator):
        for par in second:
            if(par!="timestamp"):
                for temp in second[par]:
                    if(first[par][temp]['volume']>second[par][temp]['volume']):
                        if(second[par][temp]['open']==second[par][temp]['close']):
                            #print("\t"+par+":"+temp+"-"+str(second[par][temp]['open'])+"=="+str(second[par][temp]['close']),end="")
                            #print("\t"+str(first[par][temp]['volume'])+"=="+str(second[par][temp]['volume'])+"? True",end=" ")
                            if(validator[par][temp]==False):
                                first[par][temp]['close']=second[par][temp]['open']
                                trackingData.sendData(par,temp,first[par][temp],first['timestamp'])
                                #Se envia first[par][temp] a DB y a analisis
                                #print(" SEND",end="")
                                validator[par][temp]=True
                            #print("")
        return validator

    def checkValidator(validator):
        keepChecking=False
        for par in validator:
            for temp in validator[par]:
                if(validator[par][temp]==False):
                    keepChecking=True
                    #print("Falta->"+par+temp+":"+str(validator[par][temp]),end="|")
        #print("")
        return keepChecking

    def resetValidator(intervals):
        validator={}
        for par in trackingData.pares:
            validator[par]={}
            for temp in intervals:
                validator[par][temp]=False
        return validator

    def getIntervals():
        min=int(t.time()/60)
        if(min%1440==0):
            return ['1m','5m','15m','30m','1h','2h','4h','1d']
        if(min%240==0):
            return ['1m','5m','15m','30m','1h','2h','4h']
        if(min%120==0):
            return ['1m','5m','15m','30m','1h','2h']
        if(min%60==0):
            return ['1m','5m','15m','30m','1h']
        if(min%30==0):
            return ['1m','5m','15m','30m']
        if(min%15==0):
            return ['1m','5m','15m']
        if(min%5==0):
            return ['1m','5m']
        return ['1m']

    def sendData(par,temp,data,timestamp):
        dateTake=datetime.fromtimestamp(timestamp)
        if(temp=="1m"):
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(minutes=1)
        elif(temp=="5m"):
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(minutes=5)
        elif(temp=="15m"):
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(minutes=15)
        elif(temp=="30m"):
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(minutes=30)
        elif(temp=="1h"):
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(hours=1)
        elif(temp=="2h"):
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(hours=2)
        elif(temp=="4h"):
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(hours=4)
        else:
            candeltime = datetime(dateTake.year,dateTake.month,dateTake.day,0,0,0)

        if(temp=='1m'):
            if(data['close']<data['low']):
                data['low']=data['close']

        data['name']=par
        data['temp']=temp
        data['dateT']=str(candeltime)
        data['segT']=round(float(dateTake.strftime('%S.%f')),2)
        DBReal.datatoDB(data)
        return None

    def letsexit(signum, frame):
        print ("\n\nTime to exit Main")
        sys.exit(0)

if __name__ == '__main__':
    par=["BINANCE:BTCBUSDPERP"]
    #par=['BINANCE:BTCBUSDPERP','BINANCE:ETHBUSDPERP','BINANCE:BNBBUSDPERP','BINGX:BTCUSDT']
    trackingData.init(par)
    #config.refresh()
    #trackingData(pares=config.getlist('DataTake','data_crypto'),pprint=True)
   
#INTERVAL_1_MINUTE = "1m"
#INTERVAL_5_MINUTES = "5m"
#INTERVAL_15_MINUTES = "15m"
#INTERVAL_30_MINUTES = "30m"
#INTERVAL_1_HOUR = "1h"
#INTERVAL_2_HOURS = "2h"
#INTERVAL_4_HOURS = "4h"
#INTERVAL_1_DAY = "1d"
#INTERVAL_1_WEEK = "1W"
#INTERVAL_1_MONTH = "1M"
