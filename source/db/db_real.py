from source.config.configP import config
import mysql.connector

class DBReal():    
    def createTableData():
        query="CREATE TABLE IF NOT EXISTS crypto.data(id int auto_increment primary key not null,name varchar(30) not null,temp varchar(5) not null,dateT TIMESTAMP not null,segT float(10),close float(10) not null,open float(10) not null,high float(10) not null,low float(10) not null,volume float(10) not null,BBupper float(10),BBlower float(10),RSI7 float(10),MACDmacd float(10),MACDsignal float(10));"
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
        jdata['id']=cursorDB.lastrowid
        mydb.close()

    def getData(jData):
        query="SELECT * FROM crypto.data WHERE temp='"+jData['temp']+"' and name='"+jData['name']+"' and dateT='"+str(jData['dateT'])+"';"
        mydb = DBReal.getLocalConnector()
        cursorDB = mydb.cursor()
        cursorDB.execute(query)
        myresult = cursorDB.fetchall()
        mydb.close()
        return myresult
        
    def getColumns():
        #dbColumns=DBReal.getDBcolumns() #Obtener las cokumnas de la DB para compararlas y asi agregar comuna en la DB
        #ALTER TABLE vendors ADD COLUMN phone VARCHAR(15) AFTER name;
        indic=config.getlist('DataTake','indicators')
        columns=[]
        columns.append('name')
        columns.append('temp')
        columns.append('dateT')
        columns.append('segT')
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

    def getUsersBot(bot,categoria):
        query="SELECT idChannel,timezone FROM users."+bot+" WHERE categoria='"+categoria+"';"
        mydb = DBReal.getLocalConnector()
        cursorDB = mydb.cursor()
        cursorDB.execute(query)
        myresult = cursorDB.fetchall()
        mydb.close()
        return myresult
    
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
         
        
