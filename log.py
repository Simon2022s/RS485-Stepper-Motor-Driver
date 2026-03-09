import logging as lg
import os
from logging import handlers



class MyLog:
    logger=None
    def __init__(self,name,filename='log.log'):
        self.logger = lg.getLogger(name)
        self.logger.setLevel(lg.INFO)
        format = '[%(asctime)s] [%(levelname)s] %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        log_path = os.path.join(os.getcwd(), "log")
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_filepath = os.path.join(log_path, filename)
        th = handlers.TimedRotatingFileHandler(filename=log_filepath,when='midnight',encoding='utf-8')
        th.setFormatter(lg.Formatter(format,datefmt))
        self.logger.addHandler(th)
        console = lg.StreamHandler()
        console.setLevel(lg.INFO)
        console.setFormatter(lg.Formatter(format,datefmt))
        self.logger.addHandler(console)


def getLogger(name):
    mylog=MyLog(name)
    return mylog.logger

logging=getLogger(__name__)
