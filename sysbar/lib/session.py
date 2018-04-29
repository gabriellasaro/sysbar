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
import sqlite3, json
from datetime import datetime
from platform import node
from os import remove, path
from sysbar.lib.crypt import SbCrypt
from sysbar.lib.log import SbLog
from sysbar.lib.funcbase import SbFuncBase
class SbSession(SbFuncBase):

    def check_level(self, force=False):
        if not self.check_directory('/.system-bar', '/session.json'):
            return 0
        data = open(path.abspath('..')+'/.system-bar/session.json', 'r')
        user = json.loads(data.read())
        data.close()

        if not force:
            return user['user']['level']
        else:
            conn = sqlite3.connect(path.abspath('..')+'/.system-bar/database/users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT user_level FROM sb_users WHERE username='{}' LIMIT 1".format(user['user']['username']))
            result = cursor.fetchone()
            if not result:
                return 0
            return result[0]
    
    def get_info(self):
        data = open(path.abspath('..')+'/.system-bar/session.json', 'r')
        session = data.read()
        data.close()
        return json.loads(session)

class SbLogin():

    def __init__(self, username, pin):
        self.conn = sqlite3.connect(path.abspath('..')+'/.system-bar/database/users.db')
        self.cursor = self.conn.cursor()

        self.username = username
        data = self._search_user()
        if data['rStatus']!='1':
            SbLog('O usuário ({}) não existe/desativado'.format(self.username))
            self.rStatus = {'rStatus':data['rStatus']}
            return
        
        crypt = SbCrypt()
        if not crypt.check(pin, data['data'][0]):
            SbLog('O usuário ({}) errou a senha.'.format(self.username))
            self.rStatus = {'rStatus':'4'}
            return
        
        self._create_session()
        self.conn.close()
        info = {
            'user':{
                'username': self.username,
                'name': data['data'][1],
                'level': data['data'][2],
                'info':{
                    'computer':node()
                }
            }
        }
        write = open(path.abspath('..')+'/.system-bar/session.json', 'w+')
        write.writelines(json.dumps(info))
        write.close()
        SbLog('O usuário ({}) entrou.'.format(self.username))
        self.rStatus = {'rStatus':'1'}
        return
    
    def get_status(self):
        return self.rStatus
    
    def _search_user(self):
        self.cursor.execute("SELECT user_pin, user_nicename, user_level, user_status FROM sb_users WHERE username='{}' LIMIT 1".format(self.username))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':'3'}
        if result[3] != 1:
                return {'rStatus':'10'}
        return {'rStatus':'1', 'data':result}
    
    def _create_session(self):
        self.cursor.execute("""INSERT INTO sb_sessions (username, computer_name, register)
        VALUES (?, ?, ?)""", (self.username, node(), datetime.now()))
        self.conn.commit()
        return {'rStatus':'1'}

class SbLogout():

    def __init__(self):
        data = open(path.abspath('..')+'/.system-bar/session.json', 'r')
        session = json.loads(data.read())
        data.close()
        SbLog('O usuário ({}) encerrou a sessão.'.format(session['user']['username']))
        remove(path.abspath('..')+'/.system-bar/session.json')