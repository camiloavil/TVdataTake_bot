from datetime import datetime, timedelta

class checkData():
    def check_integrity(table,lastData):
        dGap=checkData.geTimeGap(lastData['temp'])
        table.append(lastData)
        gaps=[]
        for x in range(len(table)-1):
            gapT=table[x+1]['dateT']-table[x]['dateT']
            if(gapT!=dGap):
                gaps.append({'date':table[x]['dateT']+dGap,'long':gapT-dGap-dGap,'data':table[x]})
        if(len(gaps)==0):
            return True
        else:
            return gaps

    def geTimeGap(temp):
        if(temp=='1m'):
            return timedelta(minutes=1)
        if(temp=='5m'):
            return timedelta(minutes=5)
        if(temp=='15m'):
            return timedelta(minutes=15)
        if(temp=='30m'):
            return timedelta(minutes=30)
        if(temp=='1h'):
            return timedelta(hours=1)
        if(temp=='2h'):
            return timedelta(hours=2)
        if(temp=='4h'):
            return timedelta(hours=4)
        if(temp=='1d'):
            return timedelta(days=1)
        print("Se debe especificar la temporalidad")
        return None