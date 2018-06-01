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
from random import randint
from sysbar.core.db.connect import DBSysbar
import json
class SbBNUProduct():

    def __init__(self):
        self.conn = DBSysbar().conn(False)
        self.cursor = self.conn.cursor()
    
    def get_product_id(self):
        return self.idProduct

    def set_product_id(self, idProduct):
        self.idProduct = idProduct
    
    def check_product_barcode(self, barcode):
        self.cursor.execute("SELECT ID_product FROM sb_product WHERE barcode='{}' LIMIT 1".format(barcode))
        result = self.cursor.fetchone()
        if not result:
            return False
        return True
    
    def check_product_id(self):
        self.cursor.execute("SELECT ID_product FROM sb_meta_product WHERE ID_product='{}' LIMIT 1".format(self.idProduct))
        result = self.cursor.fetchone()
        if not result:
            return False
        return True

class SbNewProduct(SbBNUProduct):

    def generate_product_id(self):
        loop = True
        while loop:
            self.set_product_id(randint(1000, 9999))
            if not self.check_product_id():
                loop = False
        return

    def insert_meta_product(self, args):
        self.generate_product_id()
        try:
            self.cursor.execute("""INSERT INTO sb_meta_product (ID_product, ID_category, virtual_menu, special_request, delivery, unity, amount, people_served) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (self.idProduct, args[0], args[1], args[2], args[3], args[4], args[5], args[6]))
            self.conn.commit()
            return [True, self.idProduct]
        except:
            return [False]
    
    def insert_product(self, args):
        if int(args[6])>=1:
            statusStock = 1
        else:
            statusStock = 0
        
        try:
            self.cursor.execute("""INSERT INTO sb_product (ID_product, barcode, product_name, product_description, product_ingre, product_price, product_cost, product_stock, stock_status, register) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.idProduct, args[0], args[1], args[2], args[3], args[4], args[5], args[6], statusStock, datetime.now()))
            self.conn.commit()
            return True
        except:
            return False

    def delete_meta_product(self):
        try:
            self.cursor.execute("DELETE FROM sb_meta_product WHERE ID_product={}".format(self.idProduct))
            self.conn.commit()
            return True
        except:
            return False

class SbUpdateProduct(SbBNUProduct):

    def update_barcode(self, barcode):
        try:
            self.cursor.execute("""UPDATE sb_product SET barcode = ?, last_change = ? WHERE ID_product = ?""", (barcode, datetime.now(), self.idProduct))
            self.conn.commit()
            return True
        except:
            return False

    def update_info(self, args):
        try:
            self.cursor.execute("""UPDATE sb_product SET product_name = ?, product_description = ?, product_ingre = ?, last_change = ? WHERE ID_product = ?""", (args[0], args[1], args[2], datetime.now(), self.idProduct))
            self.conn.commit()
            return True
        except:
            return False
    
    def update_price_stock(self, args):
        if int(args[2])>=1:
            statusStock = 1
        else:
            statusStock = 0
        
        try:
            self.cursor.execute("""UPDATE sb_product SET product_price = ?, product_cost = ?, product_stock = ?, stock_status = ?, last_change = ? WHERE ID_product = ?""", (args[0], args[1], args[2], statusStock, datetime.now(), self.idProduct))
            self.conn.commit()
            return True
        except:
            return False

    def update_technical_information(self, args):
        try:
            self.cursor.execute("""UPDATE sb_meta_product SET ID_category = ?, virtual_menu = ?, special_request = ?, delivery = ?, unity = ?, amount = ?, people_served = ? WHERE ID_product = ?""", (args[0], args[1], args[2], args[3], args[4], args[5], args[6], self.idProduct))
            self.conn.commit()

            self.cursor.execute("""UPDATE sb_product SET last_change = ? WHERE ID_product = ?""", (datetime.now(), self.idProduct))
            self.conn.commit()

            return True
        except:
            return False

    def update_discount(self, free):
        try:
            self.cursor.execute("""UPDATE sb_product SET free_volume = ?, last_change = ? WHERE ID_product = ?""", (json.dumps(free), datetime.now(), self.idProduct))
            self.conn.commit()
            return True
        except:
            return False