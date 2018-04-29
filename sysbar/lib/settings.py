# Copyright 2018 Gabriel Lasaro
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from shutil import make_archive
from datetime import datetime
import json
import os
from sysbar.lib.funcbase import SbFuncBase
class SbStoreInfo(SbFuncBase):

    def get_store_info(self):
        if not self.check_directory('/.system-bar/settings', '/store.json'):
            return {'rStatus':0}
        
        arquivo = os.path.abspath('..') + '/.system-bar/settings/store.json'
        getInfo = open(arquivo, 'r')
        data = getInfo.read()
        getInfo.close()
        if len(data.strip())==0:
            return {'rStatus':0}
        return {'rStatus':1, 'data':json.loads(data)}

    def set_store_info(self, info):
        data = {
            "store": {
                "name":info[0],
                "cnpj":info[1],
                "logradouro":info[2],
                "number":info[3],
                "cep":info[4],
                "district":info[5],
                "city":info[6],
                "state":info[7],
                "nation":info[8],
                "phone":info[9]
                }
        }
        caminho = os.path.abspath('..') + '/.system-bar/settings'
        if not os.path.exists(caminho):
            os.makedirs(caminho)
        
        try:
            arquivo = caminho + '/store.json'
            write = open(arquivo, 'w')
            write.write(json.dumps(data))
            write.close()
            return True
        except:
            return False

class SbTheme(SbFuncBase):

    def get_theme(self):
        caminho = '/.system-bar/settings'
        if not self.check_directory(caminho, '/theme.txt'):
            return False
        
        arquivo = os.path.abspath('..') + caminho + '/theme.txt'
        data = open(arquivo, 'r')
        rData = data.read()
        data.close()

        if len(rData.strip())==0:
            return False
        
        if rData=='1':
            return True
        return False
    
    def change(self, status):
        caminho = os.path.abspath('..') + '/.system-bar/settings'
        if not os.path.exists(caminho):
            os.makedirs(caminho)
        arquivo = caminho + '/theme.txt'
        statusFile = open(arquivo, 'w')
        if status:
            statusFile.write("1")
        else:
            statusFile.write("0")
        statusFile.close()

class SbBackup():

    def create(self):
        data = str(datetime.today()).replace(':', '-')
        data = data.replace('.', '-')
        data = data.replace(' ', '-')
        make_archive('backup-sysbar-{}'.format(data), 'zip', os.path.abspath('..')+'/.system-bar')