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
import json
from sysbar.core.db.connect import DBSysbar
class SbProducts():

    def __init__(self, idProduct=None):
        self.cursor = DBSysbar().conn(True)
        self.idProduct = idProduct
    
    def get_product_id(self):
        return self.idProduct

    def set_product_id(self, idProduct):
        self.idProduct = idProduct
    
    def get_product_list(self):
        self.cursor.execute("SELECT ID_product, barcode, product_name, product_price, product_stock, stock_status FROM sb_product")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

    def get_product_info(self):
        self.cursor.execute("SELECT sb_product.*, sb_meta_product.*, sb_list_categories.category FROM sb_product INNER JOIN sb_meta_product ON sb_product.ID_product=sb_meta_product.ID_product INNER JOIN sb_list_categories ON sb_meta_product.ID_category=sb_list_categories.ID_category WHERE sb_product.ID_product='{}' LIMIT 1".format(self.idProduct))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {
            'rStatus':1,
            'data':{
                'id':result[0],
                'barcode':result[1],
                'name':result[2],
                'description':result[4],
                'ingre':result[5],
                'price':result[6],
                'custPrice':result[7],
                'discount':result[8],
                'stock':result[9],
                'statusStock':result[10],
                'register':result[11],
                'lastChange':result[12],
                'virtualMenu':result[15],
                'specialRequest':result[16],
                'delivery':result[17],
                'unity':result[18],
                'amount':result[19],
                'peopleServed':result[20],
                'printer':result[21],
                'category':result[22],
                'idCategory':result[14]
            }
        }
        
    def search_product(self, code=False):
        if not code:
            self.cursor.execute("SELECT ID_product, barcode, product_name, product_img, product_price, product_discount, product_stock, stock_status FROM sb_product WHERE ID_product='{}' LIMIT 1".format(self.idProduct))
        else:
            self.cursor.execute("SELECT ID_product, barcode, product_name, product_img, product_price, product_discount, product_stock, stock_status FROM sb_product WHERE barcode='{}' LIMIT 1".format(code))            
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {'rStatus':1, 'data':result}

# Não usa a base do SbProducts
class SbWProducts():

    def __init__(self, idProduct=None):
        self.cursor = DBSysbar().conn(True)
        self.idProduct = idProduct
    
    def get_products_for_category(self, categoryId):
        self.cursor.execute("""SELECT sb_product.ID_product, sb_product.product_name, sb_product.product_description, sb_product.product_price, sb_product.product_stock, sb_product.stock_status,
sb_meta_product.unity, sb_meta_product.amount FROM sb_product INNER JOIN sb_meta_product ON sb_product.ID_product=sb_meta_product.ID_product WHERE sb_meta_product.ID_category = {} AND sb_meta_product.virtual_menu='1'""".format(categoryId))
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        
        items = {
            'rStatus':1,
            'data':[]
        }
        for x in result:
            if x[5]==1 and x[4]<=0:
                continue
            items['data'].append({
                'ID_product':x[0],
                'name':x[1],
                'description':x[2],
                'price':str(x[3]).replace(".", ","),
                'unity':x[6],
                'amount':x[7]
                })
        return items

    def get_product_simple_info(self):
        self.cursor.execute("SELECT sb_product.*, sb_meta_product.unity, sb_meta_product.amount, sb_meta_product.people_served FROM sb_product INNER JOIN sb_meta_product ON sb_meta_product.ID_product=sb_product.ID_product WHERE sb_product.ID_product='{}' LIMIT 1".format(self.idProduct))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        return {
            'rStatus':1,
            'data':{
                'id':result[0],
                'barcode':result[1],
                'name':result[2],
                'description':result[4],
                'ingre':result[5],
                'price':str(result[6]).replace(".", ","),
                'discount':json.loads(result[8]),
                'stock':result[9],
                'statusStock':result[10],
                'unity':result[13],
                'amount':str(result[14]).replace(".", ","),
                'peopleServed':result[15],
            }
        }