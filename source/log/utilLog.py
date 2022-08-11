import os,logging

def create_log(logger_name,filename,folder,level=logging.INFO):
    foldername=os.path.dirname(os.path.realpath(__file__)).replace("source/log",'')+folder+"/"
    #print(foldername)
    if os.path.exists(foldername)==False:
        os.makedirs(foldername)
    l = logging.getLogger(logger_name)
    if(l.isEnabledFor(level)==False):
        #formatter = logging.Formatter('%(asctime)s-%(name)s-%(message)s')
        #formatter = logging.Formatter('%(name)s-%(message)s')
        hdl = logging.FileHandler(foldername+filename+'.log')
        hdl.terminator = ""
        #hdl.setFormatter(formatter)
        l.addHandler(hdl)
        l.setLevel(level)
    del (l)