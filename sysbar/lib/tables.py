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
import sqlite3
from datetime import datetime, date

class SbTables():

    def __init__(self, tableId=None):
        self.conn = sqlite3.connect('/home/gabriel/.system-bar/database/sysbar.db')
        self.cursor = self.conn.cursor()
        self.tableId = tableId
    
    def set_table_id(self, tableId):
        self.tableId = tableId
    
    def get_tables_list(self):
        self.cursor.execute("SELECT ID_table, table_price, busy_table, table_capacity FROM sb_tables")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

    def search_table(self, table):
        self.cursor.execute("SELECT ID_table FROM sb_tables WHERE ID_table={}".format(table))
        result = self.cursor.fetchone()
        if not result:
            return False
        return True
    
    def update_table_status(self, active=True):
        self.cursor.execute("SELECT busy_table FROM sb_tables WHERE ID_table={} LIMIT 1".format(self.tableId))
        result = self.cursor.fetchone()
        if not result:
            return False
        
        if active:
            if result[0]==1:
                return True
        
            try:
                self.cursor.execute("""UPDATE sb_tables SET busy_table="1" WHERE ID_table={}""".format(self.tableId))
                self.conn.commit()
                return True
            except:
                return False
        else:
            if result[0]==0:
                return True
        
            try:
                self.cursor.execute("""UPDATE sb_tables SET busy_table="0" WHERE ID_table={}""".format(self.tableId))
                self.conn.commit()
                return True
            except:
                return False