import os,logging

def createAlarm_log(logger_name,filename,folder,level=logging.INFO):
    if os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/"+folder+"/"+filename[:filename.rfind("/")]+"/")==False:
        #print(os.path.dirname(os.path.realpath(__file__))+"/"+folder+"/"+filename[:filename.rfind("/")]+"/"+"   No exist")
        os.makedirs(os.path.dirname(os.path.realpath(__file__))+"/"+folder+"/"+filename[:filename.rfind("/")])
    l = logging.getLogger(logger_name)
    if(l.isEnabledFor(level)==False):
        #formatter = logging.Formatter('%(asctime)s-%(name)s-%(message)s')
        formatter = logging.Formatter('%(name)s-%(message)s')
        hdl = logging.FileHandler(os.path.dirname(os.path.realpath(__file__))+'/'+folder+"/"+filename+'.log')
        hdl.setFormatter(formatter)
        l.addHandler(hdl)
        l.setLevel(level)
    del (l)