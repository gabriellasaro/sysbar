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
from random import randint
from shutil import copyfile

class SbProducts():

    def __init__(self, idProduct=None):
        self.conn = sqlite3.connect('/home/gabriel/.system-bar/database/sysbar.db')
        self.cursor = self.conn.cursor()
        self.idProduct = idProduct
    
    def get_product_id(self):
        return self.idProduct

    def set_product_id(self, idProduct):
        self.idProduct = idProduct
    
    # ALERTA: Remover no futuro.
    def get_categories(self):
        self.cursor.execute("SELECT ID_category, category FROM sb_list_categories")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

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

    def get_product_list(self):
        self.cursor.execute("SELECT ID_product, barcode, product_name, product_price, product_discount, product_stock, stock_status FROM sb_product")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

    def get_product_information(self):
        self.cursor.execute("SELECT sb_product.*, sb_meta_product.*, sb_list_categories.category FROM sb_product INNER JOIN sb_meta_product ON sb_product.ID_product=sb_meta_product.ID_product INNER JOIN sb_list_categories ON sb_meta_product.ID_category=sb_list_categories.ID_category WHERE sb_product.ID_product='{}' LIMIT 1".format(self.idProduct))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

    def save_image(self, img, name):
        try:
            copyfile(img, "/home/gabriel/sysbar/static/{}".format(name))
            return True
        except:
            return False

    def search_product(self, code=False):
        if not code:
            self.cursor.execute("SELECT ID_product, barcode, product_name, product_img, product_price, product_discount, product_stock, stock_status FROM sb_product WHERE ID_product='{}' LIMIT 1".format(self.idProduct))
        else:
            self.cursor.execute("SELECT ID_product, barcode, product_name, product_img, product_price, product_discount, product_stock, stock_status FROM sb_product WHERE barcode='{}' LIMIT 1".format(code))            
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}
    
class SbProductInsert(SbProducts):

    def generate_product_id(self):
        loop = True
        while loop:
            self.set_product_id(randint(1000, 9999))
            if not self.check_product_id():
                loop = False
        return

    def insert_meta_product(self, cvirtual, special, delivery, unity, amount, people, category):
        self.generate_product_id()
        try:
            self.cursor.execute("""INSERT INTO sb_meta_product (ID_product, ID_category, virtual_menu, special_request, delivery, unity, amount, people_served, register) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.idProduct, category, cvirtual, special, delivery, unity, amount, people, datetime.now()))
            self.conn.commit()
            return True
        except:
            return False
    
    def insert_product(self, name, barcode, description, price, cost, img, stock, discount):
        if int(stock)>1:
            statusStock = 1
        else:
            statusStock = 0
        imgName = "products-img/{}-{}.{}".format(date.today(), self.idProduct, img[-3:])
        if not self.save_image(img, imgName):
            return False
        
        try:
            self.cursor.execute("""INSERT INTO sb_product (ID_product, barcode, product_name, product_description, product_img, product_price, product_cost, product_discount, product_stock, stock_status, register) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.idProduct, barcode, name, description, imgName, price, cost, discount, stock, statusStock, datetime.now()))
            self.conn.commit()
            self.update_status_success()
            return True
        except:
            return False
        
    def update_status_success(self):
        try:
            self.cursor.execute("UPDATE sb_meta_product SET status=1 WHERE ID_product={}".format(self.idProduct))
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

class SbProductUpdate(SbProducts):

    def update_meta_product(self, cvirtual, special, delivery, unity, amount, people, category):
        print(self.idProduct)
        try:
            self.cursor.execute("""UPDATE sb_meta_product SET ID_category = ?, virtual_menu = ?, special_request = ?, delivery = ?, unity = ?, amount = ?, people_served = ? WHERE ID_product = ?""", (category, cvirtual, special, delivery, unity, amount, people, self.idProduct))
            self.conn.commit()
            return True
        except:
            return False
    
    def update_product_s2(self, name, barcode, description, price, cost, img, stock, discount):
        if int(stock)>1:
            statusStock = 1
        else:
            statusStock = 0
        
        if img:
            imgName = "products-img/{}-{}.{}".format(date.today(), self.idProduct, img[-3:])
            if not self.save_image(img, imgName):
                return False
            
        try:
            if img:
                self.cursor.execute("""UPDATE sb_product SET barcode = ? , product_name = ?, product_description = ?, product_img = ?, product_price = ?, product_cost = ?, product_discount = ?, product_stock = ?, stock_status = ?, last_change = ? WHERE ID_product = ?""", (barcode, name, description, imgName, price, cost, discount, stock, statusStock, datetime.now(), self.idProduct))
            else:
                self.cursor.execute("""UPDATE sb_product SET barcode = ? , product_name = ?, product_description = ?, product_price = ?, product_cost = ?, product_discount = ?, product_stock = ?, stock_status = ?, last_change = ? WHERE ID_product = ?""", (barcode, name, description, price, cost, discount, stock, statusStock, datetime.now(), self.idProduct))
            self.conn.commit()
            return True
        except:
            return False

class SbCategories():

    def __init__(self, categoryId=None):
        self.conn = sqlite3.connect('/home/gabriel/.system-bar/database/sysbar.db')
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

# Não usa a base do SbProducts
class SbWProducts():

    def __init__(self, idProduct=None):
        self.conn = sqlite3.connect('/home/gabriel/.system-bar/database/sysbar.db')
        self.cursor = self.conn.cursor()
        self.idProduct = idProduct
    
    def get_products(self):
        self.cursor.execute("""SELECT sb_product.ID_product, sb_product.product_name, sb_product.product_img, sb_product.product_description, sb_product.product_price, sb_product.product_stock, sb_product.stock_status,
        sb_meta_product.unity, sb_meta_product.amount, sb_meta_product.people_served, sb_list_categories.category FROM sb_product INNER JOIN sb_meta_product ON sb_product.ID_product=sb_meta_product.ID_product INNER JOIN sb_list_categories ON sb_meta_product.ID_category=sb_list_categories.ID_category WHERE sb_meta_product.virtual_menu='1'""")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}