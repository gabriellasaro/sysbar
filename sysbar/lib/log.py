from sysbar.lib.funcbase import SbFuncBase
from datetime import datetime
import os
class SbLog(SbFuncBase):

    def __init__(self, msg):
        self.check_directory('/.system-bar/', '/log.txt')
        caminho = os.path.abspath('..')+'/.system-bar/log.txt'
        arquivo = open(caminho, 'a+')
        msg = "{} - {}\n".format(datetime.today(), msg)
        arquivo.write(msg)
        arquivo.close()
        return