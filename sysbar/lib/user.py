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
from os import path
from sysbar.lib.validation import ValidateInput
from sysbar.lib.crypt import SbCrypt
class SbUser():

    def __init__(self, userId = None):
        self.conn = sqlite3.connect(path.abspath('..')+'/.system-bar/database/users.db')
        self.cursor = self.conn.cursor()
        self.userId = userId

    def get_user_id(self):
        return self.userId
    
    def set_user_id(self, userId):
        self.userId = userId
    
    def get_id_by_username(self, username):
        self.cursor.execute("SELECT ID_user FROM sb_users WHERE username='{}' LIMIT 1".format(username))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result[0]}
    
    def get_user_list(self):
        self.cursor.execute("SELECT ID_user, username, user_nicename, user_phone, user_level FROM sb_users WHERE user_status='active'")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

    def get_user_info(self):
        self.cursor.execute("SELECT ID_user, username, user_nicename, user_phone, user_email, user_birthday, user_address FROM sb_users WHERE ID_user='{}' LIMIT 1".format(self.get_user_id()))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

class SbDUser(SbUser, ValidateInput):

    def new(self, args):
        if not self.validate_name(args[4]):
            return {'rStatus':11}
        if self.get_id_by_username(args[1])['rStatus']==0:
            if not self.validate_pin(args[2]):
                return {'rStatus':11}
            if not self.validate_name(args[0]):
                return {'rStatus':11}
            if not self.validate_date(args[6]):
                return {'rStatus':11}
            return self.insert_user(args)
        else:
            return {'rStatus':9}
    
    def insert_user(self, args):
        try:
            birthday = self.format_date(args[6])
            crypt = SbCrypt()
            self.cursor.execute("""INSERT INTO sb_users (username, user_pin, user_nicename, user_phone, user_email, user_birthday, user_level, user_register) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (args[1], crypt.encrypt(args[2]), args[0], args[4], args[5], birthday, args[3], datetime.now()))
            self.conn.commit()
            return {'rStatus':1}
        except:
            return {'rStatus':0}
    
    def insert_address(self, args):
        data = {
            'CEP':args[0],
            'house':args[1],
            'street':args[2],
            'complement':args[3],
            'district':args[4],
            'city':args[5],
            'state':args[6],
            'nation':args[7]
        }
        try:
            self.cursor.execute("""UPDATE sb_users SET user_address='{}' WHERE ID_user={}""".format(json.dumps(data), self.userId))
            self.conn.commit()
            return True
        except:
            return False

    def change_name(self, name):
        try:
            self.cursor.execute("""UPDATE sb_users SET user_nicename="{}" WHERE ID_user={}""".format(name, self.userId))
            self.conn.commit()
            return True
        except:
            return False

    def change_contacts(self, args):
        try:
            self.cursor.execute("""UPDATE sb_users SET user_phone="{}", user_email="{}" WHERE ID_user={}""".format(args[0], args[1], self.userId))
            self.conn.commit()
            return True
        except:
            return False