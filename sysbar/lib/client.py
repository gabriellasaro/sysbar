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
from datetime import datetime, date
# from platform import node
from sysbar.lib.crypt import SbCrypt
from sysbar.lib.validation import ValidateInput
from sysbar.core.tables.tables import SbTables
class SbClient():

    def __init__(self, clientId = None):
        self.conn = sqlite3.connect('/home/gabriel/.system-bar/database/sysbar.db')
        self.cursor = self.conn.cursor()
        self.clientId = clientId
    
    def get_customer_id(self):
        return self.clientId
    
    def set_customer_id(self, clientId):
        self.clientId = clientId
    
    def get_customer_list(self):
        self.cursor.execute("SELECT ID_client, client_phone, client_name, client_credit FROM sb_client")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}
    
    def get_customer_information(self, phone):
        self.cursor.execute("SELECT ID_client, client_phone, client_name, client_birthday, client_credit, last_purchase FROM sb_client WHERE client_phone='{}' LIMIT 1".format(phone))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}
    
    def get_customer_id_by_phone(self, phone):
        self.cursor.execute("SELECT ID_client FROM sb_client WHERE client_phone='{}' LIMIT 1".format(phone))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result[0]}

    def get_customer_address(self):
        self.cursor.execute("SELECT ID_address, cep, house_number, street, complement, district, city, state, comment, usage FROM sb_delivery_address WHERE ID_client='{}'".format(self.clientId))
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}
    
    def check_pin(self, pin):
        self.cursor.execute("SELECT client_pin FROM sb_client WHERE ID_client='{}' LIMIT 1".format(self.clientId))
        result = self.cursor.fetchone()
        if not result:
            return False
        # Verifica a senha
        crypt = SbCrypt()
        if crypt.check(pin, result[0]):
            return True
        else:
            return False
    
    def change_name(self, name):
        validate = ValidateInput()
        if not validate.validate_name(name):
            return False
        try:
            self.cursor.execute("""UPDATE sb_client SET client_name="{}" WHERE ID_client={}""".format(name, self.clientId))
            self.conn.commit()
            return True
        except:
            return False
    
    def change_phone_number(self, phone):
        validate = ValidateInput()
        if not validate.validate_phone(phone):
            return {'rStatus':11}
        
        if self.get_customer_id_by_phone(phone)['rStatus']==0:
            try:
                self.cursor.execute("""UPDATE sb_client SET client_phone="{}" WHERE ID_client={}""".format(phone, self.clientId))
                self.conn.commit()
                return {'rStatus':1}
            except:
                return {'rStatus':0}
        else:
            return {'rStatus':9}
    
class SbDClient(SbClient, ValidateInput):
    
    def new(self, name, phone, pin, birthday = None):
        phone = phone.strip()
        if not self.validate_phone(phone):
            return {'rStatus':11}
        if self.get_customer_id_by_phone(phone)['rStatus']==0:
            name = name.strip()
            if not self.validate_pin(pin):
                return {'rStatus':11}
            if not self.validate_name(name):
                return {'rStatus':11}
            if len(birthday)==0 or birthday==None:
                birthday = ""
            else:
                birthday = self.format_date(birthday)
            return self.insert_client(phone, name, birthday, pin)
        else:
            return {'rStatus':9}
    
    def insert_client(self, phone, name, birthday, pin):
        try:
            crypt = SbCrypt()
            self.cursor.execute("""INSERT INTO sb_client (client_phone, client_pin, client_name, client_birthday, register) 
            VALUES (?, ?, ?, ?, ?)""", (phone, crypt.encrypt(pin), name, birthday, datetime.now()))
            self.conn.commit()
            return {'rStatus':1}
        except:
            return {'rStatus':0}
        
    def new_address(self, cep, house, complement, street, district, city, state, comment):
        try:
            self.cursor.execute("""INSERT INTO sb_delivery_address (ID_client, cep, house_number, street, complement, district, city, state, comment, address_register) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.clientId, cep, house, complement, street, district, city, state, comment, datetime.now()))
            self.conn.commit()
            return True
        except:
            return False

    def delete_address(self, addressId):
        try:
            self.cursor.execute("DELETE FROM sb_delivery_address WHERE ID_address={}".format(addressId))
            self.conn.commit()
            return True
        except:
            return False
    
    def update_pin(self, newPin):
        try:
            crypt = SbCrypt()
            self.cursor.execute("""UPDATE sb_client SET client_pin="{}" WHERE ID_client={}""".format(crypt.encrypt(newPin), self.clientId))
            self.conn.commit()
            return True
        except:
            return False

class SbWClient(SbClient, ValidateInput):

    def new_account(self, name, phone, pin):
        self.phone = phone
        if not self.validate_phone(self.phone):
            return {'rStatus':11}
        
        if self.get_customer_id_by_phone(self.phone)['rStatus']==0:
            self.name = name
            if not self.validate_pin(pin):
                return {'rStatus':11}
            if not self.validate_name(self.name):
                return {'rStatus':11}
            return self.insert_client(pin)
        else:
            return {'rStatus':9}
    
    def insert_client(self, pin):
        try:
            crypt = SbCrypt()
            self.cursor.execute("""INSERT INTO sb_client (client_phone, client_pin, client_name, register)
            VALUES (?, ?, ?, ?)""", (self.phone, crypt.encrypt(pin), self.name, datetime.now()))
            self.conn.commit()
            return {'rStatus':1}
        except:
            return {'rStatus':0}
    
    def login(self, phone, pin, table):
        if len(table)==0:
            return {'rStatus':11}
        self.phone = phone
        if not self.validate_phone(self.phone):
            return {'rStatus':11}
        
        result = self.get_customer_information(self.phone)
        if result['rStatus']==0:
            return {'rStatus':3}
        else:
            self.set_customer_id(result['data'][0])
            if not self.validate_pin(pin):
                return {'rStatus':11}
            # Verifica a senha
            if self.check_pin(pin):
                resultTable = SbTables(table)
                if not resultTable.update_table_status():
                    return {'rStatus':11}
                return {
                    'rStatus':1, 'user':{
                        'id':result['data'][0],
                        'name':result['data'][2],
                        }
                    }
            else:
                return {'rStatus':4}

    # def search_session(self):
    #     self.cursor.execute("SELECT ID_session, computer_name FROM sb_user_sessions WHERE username='{}' AND computer_name='{}' AND session_status='1'".format(self.username, node()))
    #     results = self.cursor.fetchall()
    #     if not results:
    #         return self.create_session()
    #     for row in results:
    #         self.close_session(row[0])
    #     return self.create_session()
    
    # def create_session(self):
    #     self.cursor.execute("""INSERT INTO sb_user_sessions (username, computer_name, register)
    #     VALUES (?, ?, ?)""", (self.username, node(), datetime.now()))
    #     self.conn.commit()
    #     return {'rStatus':'1'}
    
    # def close_session(self, IDsession):
    #     self.cursor.execute("UPDATE sb_user_sessions SET session_status='0', logout_date='{}' WHERE ID_session={}".format(datetime.now(), IDsession))
    #     self.conn.commit()