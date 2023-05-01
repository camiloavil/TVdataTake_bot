from source.config.configP import config
from source.binance.takeDataBinance import getBinanceData
import mysql.connector

class DBReal():    
    def createTableData():
        query="CREATE TABLE IF NOT EXISTS crypto.data(name varchar(30) not null,temp varchar(5) not null,dateT TIMESTAMP not null,segT float(10),close float(10) not null,open float(10) not null,high float(10) not null,low float(10) not null,volume float(10) not null,BBupper float(10),BBlower float(10),RSI7 float(10),RSI float(10),Type varchar(5),PRIMARY KEY(name,temp,dateT));"
        mydb = DBReal.getLocalConnector()
        cursorDB = mydb.cursor()
        try:
            cursorDB.execute(query)
        except:
            mydb.close()
            return False
        mydb.close()
        return True

    def datatoDB(jdata):
        columns=DBReal.getColumns()
        keys =  tuple(jdata[c] for c in columns[0])
        #print (str(keys))
        mydb = DBReal.getLocalConnector()
        #mydb = mysql.connector.connect(host="localhost",user="usPython",password="!pyUserthon1987",database = "crypto")
        cursorDB = mydb.cursor()
        #sql = "INSERT INTO data(name,temp,dateT,segT,close,open,high,low,BBupper,BBlower,RSI7,MACDmacd,MACDsignal,volume) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql = "INSERT INTO crypto.data("+columns[1]+") VALUES ("+columns[2]+")"
        cursorDB.execute(sql, keys)
        mydb.commit()
        mydb.close()
        #jdata['id']=cursorDB.lastrowid

    def datatoDBArray(arrayData):
        columns=DBReal.getColumns("BINANCE")
        keys=[]
        for data in arrayData:
            keys.append(tuple(data[c] for c in columns[0]))
        mydb = DBReal.getLocalConnector()
        cursorDB = mydb.cursor()
        sql = "INSERT INTO crypto.data("+columns[1]+") VALUES ("+columns[2]+")"
        cursorDB.executemany(sql,keys)
        mydb.commit()
        mydb.close()

    def getData(jData,nLimit):
        query="SELECT name,temp,dateT,segT,"+config.getlisttxt('DataTake','indicators').replace('.','')+" FROM crypto.data WHERE temp='"+jData['temp']+"' and name='"+jData['name']+"' and dateT<='"+str(jData['dateT'])+"'ORDER BY dateT DESC LIMIT "+str(nLimit)+";"
        mydb = DBReal.getLocalConnector()
        cursorDB = mydb.cursor()
        cursorDB.execute(query)
        myresult = cursorDB.fetchall()
        mydb.close()
        columns=config.getlist('DataTake','indicators')
        data=[]
        for xx in range(len(myresult)):
            jData={}
            jData['name']=myresult[xx][0]
            jData['temp']=myresult[xx][1]
            jData['dateT']=myresult[xx][2]
            jData['segT']=myresult[xx][3]
            #if(xx==0):
            for i in range(len(columns)):
                jData[columns[i].replace('.','')]=myresult[xx][i+4]
            data.append(jData)
        data.reverse()
        return data
        
    def getColumns(item="TV"):
        #dbColumns=DBReal.getDBcolumns() #Obtener las cokumnas de la DB para compararlas y asi agregar comuna en la DB
        #ALTER TABLE vendors ADD COLUMN phone VARCHAR(15) AFTER name;
        if "TV"==item:
            indic=config.getlist('DataTake','indicators')
        elif "BINANCE"==item:
            indic=getBinanceData.getColumns()
        else:
            return None
        columns=[]
        columns.append('name')
        columns.append('temp')
        columns.append('dateT')
        columns.append('segT')
        columns.append('Type')
        for ind in indic:
            columns.append(ind.replace('.',''))
        #print(columns)
        #print(dbColumns)
        names=""
        namescod=""
        for col in columns:
            names=names+","+col
            namescod=namescod+",%s"
        return [columns,names[1:],namescod[1:]]
    
    def getDBcolumns():
        query="select COLUMN_NAME from information_schema.columns WHERE TABLE_SCHEMA='crypto'and TABLE_NAME='data';"
        mydb = DBReal.getLocalConnector()
        cursorDB = mydb.cursor()
        cursorDB.execute(query)
        myresult = cursorDB.fetchall()
        mydb.close()
        dbColumns=[]
        for cl in myresult:
            dbColumns.append(cl[0])
        return dbColumns[1:]
            
    def getRemoteConnector():
        return mysql.connector.connect(host=config['DBremote']['host'],user=config['DBremote']['user'],password=config['DBremote']['pass'],database=config['DBremote']['dbase'])
    def getLocalConnector():
        return mysql.connector.connect(host=config['DB']['host'],user=config['DB']['user'],password=config['DB']['pass'],database=config['DB']['dbase'])
         
        
