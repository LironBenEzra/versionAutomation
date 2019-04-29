import iis_bridge
import wmi
import logging
import os
import win32serviceutil

class Services:

    def __init__(self,log_path):
        logging.basicConfig(filename=log_path, level=logging.WARNING)
    def stop_iis(self):
        iis_bridge.stop()
        logging.warn("iis is stoped!")


    def start_iis(self):
        iis_bridge.start()
        logging.warn("iis is started!")


    def service_stop(self,serviceName):
        #if action=true stop the service, else- start the service
        try:
            win32serviceutil.StopService(serviceName)
            logging.warn("Stop this service: "+serviceName)
        except:
            logging.warn('this service is already stoped')    

    def process_stop(self,processName):
            #if action=true stop the service, else- start the service
            try:
                os.system("taskkill /im {} /F".format(processName))
                logging.warn("Stop this process: "+processName)
            except:
                logging.warn('this process is already stoped')    



    def service_start(self,serviceName):
        #if action=true stop the service, else- start the service
        try:
            win32serviceutil.StartService(serviceName)
            logging.warn("Start this service: "+serviceName)
        except:
            logging.warn('this service is already started')    
