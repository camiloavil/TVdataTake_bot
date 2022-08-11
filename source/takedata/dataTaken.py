import sys, signal,logging, json
import time as t
import threading as th
from math import floor
from source.db.db_real import DBReal
from source.config.configP import config
from source.log.utilLog import create_log
from datetime import datetime, timedelta
from source.takedata.TradingViewData import data_TradingV

class trackingData():
    pares=None
    temps=None
    timer=None
    dataTake=None
    dataA=None
    dataB=None
    log=None
    def init():
        trackingData.UpdatePares()
        signal.signal(signal.SIGINT, trackingData.letsexit)
        signal.signal(signal.SIGTERM,trackingData.letsexit)
        DBReal.createTableData()
        create_log("data","data","logs")
        trackingData.log=logging.getLogger("data")
        trackingData.log.info("Init Taken Data\n")
        trackingData.dataA=trackingData.dataTake.get_indicators(trackingData.temps,config.getlist('DataTake','indicators'))
        t.sleep(10)
        #t.sleep((60-t.time()%60)+0) #sleep to the start of next min
        trackingData.run()

    def run():
        trackingData.timer=th.Timer(10,trackingData.run)
        trackingData.timer.start()
        trackingData.getData()
    
    def getData():
        trackingData.log.info("----------\t\t\t----------\t\t\t----------\t\t\t----------\t\t\t----------\t\t\t----------\t\t\t----------\t\t\t----------\t\t\t----------\n")
        trackingData.dataB=trackingData.dataTake.get_indicators(trackingData.temps,config.getlist('DataTake','indicators'))
        trackingData.checkData()
        trackingData.dataA=trackingData.dataB

    def checkData():
        jsendData={}
        for par in trackingData.pares:
            trackingData.logRows(par)
            trackingData.log.info('{:^21}|{:^4}|'.format("Analisis",'R'))
            for temp in trackingData.temps:
                if((trackingData.dataA[par][temp]['volume']>trackingData.dataB[par][temp]['volume']) and (trackingData.dataB[par][temp]['open']==trackingData.dataB[par][temp]['close'])):
                    trackingData.dataA[par][temp]['close']=trackingData.dataB[par][temp]['open']
                    dTime=trackingData.getCandleTime(temp,trackingData.dataB['timestamp'])
                    isSend=trackingData.sendData(par,temp,dTime,round(float(datetime.fromtimestamp(trackingData.dataB['timestamp']).strftime('%S.%f')),2),trackingData.dataA[par][temp])
                    try:
                        jsendData[par][temp]=dTime.strftime('%H:%M')+" "+str(isSend)
                    except:
                        jsendData[par]={}
                        jsendData[par][temp]=dTime.strftime('%H:%M')+" "+str(isSend)
                    trackingData.log.info('{:^30}|'.format(temp+" SEND IT- "+datetime.fromtimestamp(trackingData.dataB['timestamp']).strftime('%H:%M %S')))            
                else:
                    trackingData.log.info('{:^30}|'.format("No yet WAIT!!!"))            
            trackingData.log.info(par+"\n")
        if(len(jsendData)>0):
            trackingData.printSents(jsendData)

    def printSents(jData):
        print("Cycle "+datetime.fromtimestamp(trackingData.dataB['timestamp']).strftime('%Y-%m-%d %H:%M %S')+"seg Sents...")
        for par in jData:
            for temp in jData[par]:
                print('\t{:25} {:^5} {:10}'.format(par,temp,jData[par][temp]))

    def logRows(par):
        trackingData.logTitles(par)
        trackingData.log.info('{:^21}|{:^4}|'.format(par,round(trackingData.dataA['timestamp']%60,1)))
        for temp in trackingData.dataA[par]:
            trackingData.log.info('{:^10}|{:^10}|{:^8}|'.format(trackingData.dataA[par][temp]["close"],trackingData.dataA[par][temp]["open"],floor(trackingData.dataA[par][temp]["volume"])))
        trackingData.log.info(datetime.fromtimestamp(trackingData.dataA['timestamp']).strftime('%H:%M %S.%f')+"\n")
        trackingData.log.info('{:^21}|{:^4}|'.format(par,round(trackingData.dataB['timestamp']%60,1)))
        for temp in trackingData.dataB[par]:
            trackingData.log.info('{:^10}|{:^10}|{:^8}|'.format(trackingData.dataB[par][temp]["close"],trackingData.dataB[par][temp]["open"],floor(trackingData.dataB[par][temp]["volume"])))
        trackingData.log.info(datetime.fromtimestamp(trackingData.dataB['timestamp']).strftime('%H:%M %S.%f')+"\n")
    
    def logTitles(par):
        trackingData.log.info('{:^21}|{:^4}|'.format(datetime.fromtimestamp(trackingData.dataA['timestamp']).strftime('%Y-%m %H:%M'),' '))
        for temp in trackingData.temps:
            trackingData.log.info('{:^30}|'.format(trackingData.getCandleTime(temp,trackingData.dataB['timestamp']).strftime('%H:%M')+" - "+temp))
        trackingData.log.info(par+"\n")
        trackingData.log.info('{:^21}|{:^4}|'.format('PAR','Seg'))
        for x in range(len(trackingData.temps)):
            trackingData.log.info('{:^10}|{:^10}|{:^8}|'.format('close','open','vol'))
        trackingData.log.info(par+"\n")

    def getIntervals():
        min=int(t.time()/60)
        #if(min%1440==0):
        #    return ['1m','5m','15m','30m','1h','2h','4h','1d']
        if(min%240==0):
            return ['1m','5m','15m','30m','1h','2h','4h','1d']
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

    def sendData(par,temp,date,segT,data):
        if(temp=='1m'):
            if(data['close']<data['low']):
                data['low']=data['close']

        data['name']=par
        data['temp']=temp
        data['dateT']=str(date)
        data['segT']=segT
        isSave=DBReal.getData(data)
        if(len(isSave)==0):
            DBReal.datatoDB(data)
            return True
        else:
            print(isSave)
            print(data)
            return False

    def getCandleTime(temp,timestamp):
        dateTake=datetime.fromtimestamp(timestamp)
        if(temp=="1m"):
            return datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,dateTake.minute,0) - timedelta(minutes=1)
        elif(temp=="5m"):
            return datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,5*floor(dateTake.minute/5),0) - timedelta(minutes=5)
        elif(temp=="15m"):
            return datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,15*floor(dateTake.minute/15),0) - timedelta(minutes=15)
        elif(temp=="30m"):
            return datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,30*floor(dateTake.minute/30),0) - timedelta(minutes=30)
        elif(temp=="1h"):
            return datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,0,0) - timedelta(hours=1)
        elif(temp=="2h"):
            return datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,0,0) - timedelta(hours=2)
        elif(temp=="4h"):
            return datetime(dateTake.year,dateTake.month,dateTake.day,dateTake.hour,0,0) - timedelta(hours=4)
        else:
            return datetime(dateTake.year,dateTake.month,dateTake.day,0,0,0)

    def UpdatePares():
        config.refresh()
        new_pares=config.getlist('DataTake','data_crypto')
        new_temps=config.getlist('DataTake','temps')
        if(new_pares!=trackingData.pares):
            print("Check: "+str(new_pares))
        if(new_temps!=trackingData.temps):
            print("Check temps: "+str(new_temps))
        trackingData.temps=new_temps
        trackingData.pares=new_pares
        trackingData.dataTake=data_TradingV(cryptosymbol=trackingData.pares ,timeout=2)

    def letsexit(signum, frame):
        print ("\n\nTime to exit Main")
        sys.exit(0)

if __name__ == '__main__':
    trackingData.init()
   
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
