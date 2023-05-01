
class getData():
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
        if(config.getboolean("DataTake","debug")): 
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