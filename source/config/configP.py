import os, configparser

class myconfig(configparser.ConfigParser):
    def __init__(self,file_):
        configparser.ConfigParser.__init__(self)
        self.file=file_
    def refresh(self):
        config.read(self.file)
    def getlist(self,section,key):
        txt=self[section][key]
        if(txt[0]!='[' or txt[-1]!=']'):
            return None
        return txt[1:-1].replace('\n','').split(',')
    def getlistNumber(self,section,key):
        txt=self[section][key]
        if(txt[0]!='[' or txt[-1]!=']'):
            return None
        lis=txt[1:-1].replace('\n','').split(',')
        return[int(i) for i in lis]
    def getint(self,section,key):
        txt=self[section][key].split('#')[0]
        return int(txt)
    def getfloat(self,section,key):
        txt=self[section][key].split('#')[0]
        return float(txt)
    def isinTxtList(self,section,key,value):
        try:
            txt=self[section][key]
        except:
            return False
        if(txt[0]!='[' or txt[-1]!=']'):
            return False
        datos=txt[1:-1].replace('\n','').split(',')
        for dat in datos:
            if(value==dat):
                return True
        return False

config = myconfig(os.path.dirname(os.path.realpath(__file__)).replace("source/config","config.cfg"))


if __name__ == '__main__':
    config.refresh()
    print("Existe "+str(config.has_section('BINANCE:BTCBUSDPERP')))
    #print(config['Telegram']['tg_token'])
    #print(config.getlist('DataTake','indicators'))
    #print(config.getint('Telegram','kmichannel'))
    #print(config.getlist('DataTake','data_crypto'))
    #print(config.getlistNumber('BINGX:BTCUSDT', "tg_channels"))
    print(config.getint('Analisis','n_maxTPsl'))
