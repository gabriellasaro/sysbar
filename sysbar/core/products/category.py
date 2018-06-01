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
from datetime import datetime
from sysbar.core.db.connect import DBSysbar
class SbCategory():

    def __init__(self, categoryId=None):
        self.conn = DBSysbar().conn()
        self.cursor = self.conn.cursor()
        self.categoryId = categoryId
    
    def set_category_id(self, categoryId):
        self.categoryId = categoryId
    
    def get_categories(self):
        self.cursor.execute("SELECT ID_category, category FROM sb_list_categories")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

    def insert_category(self, name):
        try:
            self.cursor.execute("""INSERT INTO sb_list_categories (category, register) 
            VALUES (?, ?)""", (name, datetime.now()))
            self.conn.commit()
            return True
        except:
            return False
    
    def update_category(self, name):
        print(self.categoryId)
        try:
            self.cursor.execute("""UPDATE sb_list_categories SET category = ?, register = ? WHERE ID_category = ?""", (name, datetime.now(), self.categoryId))
            self.conn.commit()
            return True
        except:
            return False