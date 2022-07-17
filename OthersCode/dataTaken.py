import sys
import json
import time as t
import threading as th
import signal,os
import handlerServer 
from TradingViewData import data_TradingV
from configP import config
from datetime import datetime, timedelta
from db.db_real import DBReal

class tracking_price():
    def __init__(self,pares,pprint=False):
        self.crypto_data=data_TradingV(cryptosymbol=pares ,timeout=2)
        signal.signal(signal.SIGINT, self.letsexit)
        signal.signal(signal.SIGTERM,self.letsexit)
        config.refresh()
        self.pprint_=pprint
        self.keep_run=True
        for par in pares:
            print("Check "+par+" started")
        self.run()
    
    def run(self):
        t_min=61
        while self.keep_run:
            self.waitUntilsec(0)
            min=int(t.time()/60)
            #print("Inicio\t"+str(datetime.now()))   #Se usa para calibrar los tiempos
            if(((min)%(1440))==0):
                jdata1d=self.check("1d")
            if(((min)%(240))==0):
                jdata4h=self.check("4h")
            if(((min)%120)==0):
                jdata2h=self.check("2h")
            if(((min)%60)==0):
                jdata1h=self.check("1h")
            if(((min)%30)==0):
                jdata30m=self.check("30m")
            self.waitUntilmicro(9)
            if(((min)%15)==0):
                jdata15m=self.check("15m")
            if(((min)%5)==0):
                jdata5m=self.check("5m")
            if (config.getboolean('DataTake','get_m1') and (min!=t_min)):
                jdata1m=self.check("1m")
                self.send_data(jdata1m,"1m")
                del(jdata1m)
                t_min=min
            if(((min)%(1440))==0):
                self.send_data(jdata1d,"1d")
                del(jdata1d)
            if(((min)%(240))==0):
                self.send_data(jdata4h,"4h")
                del(jdata4h)
            if(((min)%120)==0):
                self.send_data(jdata2h,"2h")
                del(jdata2h)
            if(((min)%60)==0):
                self.send_data(jdata1h,"1h")
                del(jdata1h)
            if(((min)%30)==0):
                self.send_data(jdata30m,"30m")
                del(jdata30m)
            if(((min)%15)==0):
                self.send_data(jdata15m,"15m")
                del(jdata15m)
            if(((min)%5)==0):
                self.send_data(jdata5m,"5m")
                del(jdata5m)

            #self.waitUntilsec(12)
            #print("FIN\t"+str(datetime.now()))
            config.refresh()       #actulizar config
            if ((((min)%5)==0) and config.getboolean('DataTake','get_m1')==False):
                t.sleep(285) #Segundos de espera hasta los siguientes 5 min
            else:
                t.sleep(45)
                #self.waitUntilsec(30)

        
    def check(self,interval_):
        data=self.crypto_data.get_indicators(interval=interval_,indicators=config.getlist('DataTake','indicators'))
        t.sleep(0.05)
        return data

    def send_data(self,jdata,interval):
        #print(str(jdata))
        for par in self.crypto_data.cryptosymbol:
            #xnow=datetime.strptime(jdata[par]["dateTaken"],"%Y-%m-%d %H:%M:%S.%f")
            xnow=datetime.fromtimestamp(jdata[par]["dataTaken"])
            if(interval=="5m"):
                if(xnow.minute%5==0):
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,xnow.minute,0) - timedelta(minutes=5)
                else:
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,xnow.minute,0) - timedelta(minutes=4)
            elif(interval=="15m"):
                if(xnow.minute%15==0):
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,xnow.minute,0) - timedelta(minutes=15)
                else:
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,xnow.minute,0) - timedelta(minutes=14)
            elif(interval=="30m"):
                if(xnow.minute%30==0):
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,xnow.minute,0) - timedelta(minutes=30)
                else:
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,xnow.minute,0) - timedelta(minutes=29)
            elif(interval=="1h"):
                if(xnow.minute==0):
                    candeltime = datetime(xnow.year, xnow.month,xnow.day,xnow.hour,0,0) - timedelta(hours=1)
                else:
                    candeltime = datetime(xnow.year, xnow.month,xnow.day,xnow.hour,0,0)
            elif(interval=="2h"):
                if(xnow.minute==0):
                    candeltime = datetime(xnow.year, xnow.month,xnow.day,xnow.hour,0,0) - timedelta(hours=2)
                else:
                    candeltime = datetime(xnow.year, xnow.month,xnow.day,xnow.hour,0,0) - timedelta(hours=1)
            elif(interval=="4h"):
                if(xnow.minute==0):
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,xnow.minute,0) - timedelta(hours=4)
                else:
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,xnow.hour,0,0) - timedelta(hours=3)
            elif(interval=="1d"):
                    candeltime = datetime(xnow.year,xnow.month,xnow.day,0,0,0)
            else:
                candeltime = datetime(xnow.year, xnow.month,xnow.day,xnow.hour,xnow.minute,0)

            jdata[par].update({"date":str(candeltime)})
            jdata[par].update({"name":par})

            DBReal.datatoDB(name=par,temp=interval,date=candeltime,secs=float(xnow.strftime('%S.%f' )),jdata=jdata[par]['data'])

            if(config.has_section(par)):
                if(config.isinTxtList(par,'check',interval)):
                    th.Thread(target=handlerServer.trackingAlert,args=("local",json.dumps(jdata[par]),)).start()
                        
            if self.pprint_:
                print(par+"-"+interval+" Data stored:"+str(datetime.now()))
    
    def waitUntilsec(self,seconds):
        sec=int(t.time()%60)
        while (sec!=seconds and self.keep_run):
            sec=int(t.time()%60)

    def waitUntilmicro(self,micro):
        msec=datetime.now().microsecond
        while (msec<(micro*100000)):
            msec=datetime.now().microsecond

    def letsexit(self,signum, frame):
        print ("\n\nTime to exit Main")
        self.keep_run=False
        sys.exit(0)

if __name__ == '__main__':
    par=["BINANCE:BTCBUSDPERP"]
    tracking_price(par,pprint=True)
    #config.refresh()
    #tracking_price(pares=config.getlist('DataTake','data_crypto'),pprint=True)
   
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
