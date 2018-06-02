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
from datetime import datetime, date
from sysbar.core.db.connect import DBSysbar
class SbTables():

    def __init__(self, tableId=None):
        self.conn = DBSysbar().conn()
        self.cursor = self.conn.cursor()
        self.tableId = tableId
    
    def set_table_id(self, tableId):
        self.tableId = tableId
    
    def get_table_id(self):
        return self.tableId
    
    def get_tables_list(self):
        self.cursor.execute("SELECT ID_table, table_price, busy_table, table_capacity FROM sb_tables")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

    def search_table(self, tableId):
        self.cursor.execute("SELECT ID_table FROM sb_tables WHERE ID_table={}".format(tableId))
        result = self.cursor.fetchone()
        if not result:
            return False
        return True

class SbNewTable(SbTables):

    # retornar: 4 já existe;
    # retornar: 1 inserido/atualizado com sucesso;
    # retornar: 0 erro ao inserir/atualizar.
    def insert_table(self, args):
        if self.search_table(self.tableId):
            return {'rStatus':4}
        
        try:
            self.cursor.execute("""INSERT INTO sb_tables (ID_table, table_price, table_capacity, register, last_change) 
VALUES (?, ?, ?, ?, ?)""", (self.tableId, args[0], args[1], datetime.now(), datetime.now()))
            self.conn.commit()
            return {'rStatus':1}
        except:
            return {'rStatus':0}
    
    def update_table(self, args):
        if self.search_table(args[0]):
            return {'rStatus':4}
        
        try:
            self.cursor.execute("""UPDATE sb_tables SET ID_table = ?, table_price = ?, table_capacity = ?, last_change = ? WHERE ID_table = ?""", (args[0], args[1], args[2], datetime.now(), self.tableId))
            self.conn.commit()
            return {'rStatus':1}
        except:
            return {'rStatus':0}

    # def update_table_status(self, active=True):
    #     self.cursor.execute("SELECT busy_table FROM sb_tables WHERE ID_table={} LIMIT 1".format(self.tableId))
    #     result = self.cursor.fetchone()
    #     if not result:
    #         return False
        
    #     if active:
    #         if result[0]==1:
    #             return True
        
    #         try:
    #             self.cursor.execute("""UPDATE sb_tables SET busy_table="1" WHERE ID_table={}""".format(self.tableId))
    #             self.conn.commit()
    #             return True
    #         except:
    #             return False
    #     else:
    #         if result[0]==0:
    #             return True
        
    #         try:
    #             self.cursor.execute("""UPDATE sb_tables SET busy_table="0" WHERE ID_table={}""".format(self.tableId))
    #             self.conn.commit()
    #             return True
    #         except:
    #             return False