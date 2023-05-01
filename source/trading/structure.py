#from source.trading.candle import candle
from source.trading.constants import candle_color,deltaPrice
#import numpy as np

class structure():
    limit=30
    strucBullish=[]
    strucBearish=[]
    min=[]
    max=[]
    def setLimit(limit):
        structure.limit=limit

    def checkArray(dataArray,initData):
        for candle in dataArray:
            print("Check Min Max:"+str(initData['dateT'])+" - "+str(candle['dateT']))
            structure.check(initData,candle)
            print("Candle after Structuerd: "+str(candle))
            initData=candle
        return initData

    def check(candleBefore,candle):
        colorCandle=[structure.getColor(candleBefore),structure.getColor(candle)]
        if(colorCandle[0]==candle_color.AZUL):
            if(colorCandle[1]==candle_color.ROJA):
                structure.addMax(candle)
            else:
                candle['Type']=deltaPrice.NUP.name
        elif(colorCandle[0]==candle_color.ROJA):
            if(colorCandle[1]==candle_color.AZUL):
                structure.addMin(candle)
            else:
                candle['Type']=deltaPrice.NDO.name
        
    def addMax(candle):
        if(structure.isUpUp(candle['open'])):  #check alto mas alto
            candle['Type']=deltaPrice.UPUP.name
        else:
            candle['Type']=deltaPrice.UP.name
        ##Add maximo al array
        structure.max.insert(0,{"value":candle['open'],"date":candle['dateT'],"Type":candle['Type']})
        if(len(structure.max)>structure.limit):
            structure.max.pop(structure.limit)
        #print("add Max: "+str(structure.max[0]))

    def addMin(candle):
        if(structure.isDownDown(candle['open'])): #check bajo mas bajo
            candle['Type']=deltaPrice.DODO.name
        else:
            candle['Type']=deltaPrice.DO.name
        ##Add minimo al array
        structure.min.insert(0,{"value":candle['open'],"date":candle['dateT'],"Type":candle['Type']})
        if(len(structure.min)>structure.limit):
            structure.min.pop(structure.limit)
        #print("add Min: "+str(structure.min[0]))

    def isDownDown(valorMIN): #check bajo mas bajo
        if(len(structure.min)>0):
            print("Es "+str(valorMIN)+" Bajo mas bajo?",end="")
            min=structure.min[0]['value']
            for dat in structure.min:
                if(dat['value']<min):
                    min=dat['value']
            if(valorMIN<min):
                print("YEAH!!!!!!!!!!")
                structure.strucBearish.append(structure.max[0]['value']) #add Structure
                return True
        return False

    def isUpUp(valorMAX): #check bajo mas bajo
        if(len(structure.max)>0):
            print("Es "+str(valorMAX)+" Alto mas alto?",end="")
            max=structure.max[0]['value']
            for dat in structure.max:
                if(dat['value']>max):
                    max=dat['value']
            if(valorMAX>max):
                print("YEAH!!!!!!!!!!")
                structure.strucBullish.append(structure.min[0]['value']) #add Structure
                return True
        return False

    def getColor(jdata):
        if(jdata['close']>=jdata['open']):
            return candle_color.AZUL
        else:
            return candle_color.ROJA

    def printall():
        for x in range(len(structure.min)):
            print('|{:^5}'.format(x),end="")
        print('|')
        for dat in structure.min:
            print('|{:^5}'.format(dat['value']),end="")
            #print(dat['value'],end="")
        print("|\tMinimos")
        for dat in structure.min:
            print('|{:^5}'.format(dat['type'].name),end="")
            #print(dat['value'],end="")
        print("|\tTypes Minimos")
        for dat in structure.max:
            print('|{:^5}'.format(dat['value']),end="")
            #print(dat['value'],end="")
        print("|\tMaximos")
        for dat in structure.max:
            print('|{:^5}'.format(dat['type'].name),end="")
            #print(dat['value'],end="")
        print("|\tMaximos")
        print("Estructura Bajista: "+str(structure.strucBearish))
        print("Estructura Alcista: "+str(structure.strucBullish))