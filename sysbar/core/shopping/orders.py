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
class SbOrders():

    def __init__(self, orderId=None):
        self.conn = DBSysbar().conn()
        self.cursor = self.conn.cursor()
        self.orderId = orderId
    
    def set_order_id(self, orderId):
        self.orderId = orderId
    
    def get_order_id(self):
        return self.orderId
    
    def get_orders_list(self):
        self.cursor.execute("SELECT sb_orders.ID_order, sb_orders.ID_comanda, sb_comandas.ID_table, sb_client.client_name, sb_product.ID_product, sb_product.product_name, sb_meta_product.printer, sb_orders.amount, sb_orders.comment, sb_orders.register FROM sb_orders INNER JOIN sb_comandas ON sb_orders.ID_comanda=sb_comandas.ID_comanda INNER JOIN sb_client ON sb_comandas.ID_client=sb_client.ID_client INNER JOIN sb_product ON sb_orders.ID_product=sb_product.ID_product INNER JOIN sb_meta_product ON sb_product.ID_product=sb_meta_product.ID_product WHERE order_status=1")
        result = self.cursor.fetchall()
        if not result:
            return {'rStatus':0}
        
        items =  {
            'rStatus':1,
            'data':{}
        }

        for x in result:
            if x[1] in items['data']:
                if x[6] == 1:
                    items['data'][x[1]]['printer'].append({
                        'ID_order':x[0],
                        'ID_product':x[4],
                        'name':x[5],
                        'amount':x[7],
                        'comment':x[8],
                        'register':x[9]
                        })
                else:
                    items['data'][x[1]]['items'].append({
                        'ID_order':x[0],
                        'ID_product':x[4],
                        'name':x[5],
                        'amount':x[7],
                        'comment':x[8],
                        'register':x[9]
                        })
            else:
                items['data'][x[1]] = {
                    'ID_comanda':x[1],
                    'ID_table':x[2],
                    'client_name':x[3],
                    'printer':[],
                    'items':[]
                }
                if x[6] == 1:
                    items['data'][x[1]]['printer'].append({
                        'ID_order':x[0],
                        'ID_product':x[4],
                        'name':x[5],
                        'amount':x[7],
                        'comment':x[8],
                        'register':x[9]
                        })
                else:
                    items['data'][x[1]]['items'].append({
                        'ID_order':x[0],
                        'ID_product':x[4],
                        'name':x[5],
                        'amount':x[7],
                        'comment':x[8],
                        'register':x[9]
                        })
        return items
    
    def get_order_info(self):
        self.cursor.execute("SELECT sb_orders.ID_order, sb_orders.ID_comanda, sb_comandas.ID_table, sb_client.ID_client, sb_client.client_name, sb_product.ID_product, sb_product.product_name, sb_orders.price, sb_orders.amount, sb_orders.discount, sb_orders.shared, sb_orders.comment, sb_orders.order_status, sb_orders.register FROM sb_orders INNER JOIN sb_comandas ON sb_orders.ID_comanda=sb_comandas.ID_comanda INNER JOIN sb_client ON sb_comandas.ID_client=sb_client.ID_client INNER JOIN sb_product ON sb_orders.ID_product=sb_product.ID_product INNER JOIN sb_meta_product ON sb_product.ID_product=sb_meta_product.ID_product WHERE ID_order={} LIMIT 1".format(self.orderId))
        result = self.cursor.fetchone()
        if not result:
            return {'rStatus':0}
        
        return {
            'rStatus':1,
            'data':{
                'ID_comanda':result[1],
                'ID_table':result[2],
                'ID_client':result[3],
                'client_name':result[4],
                'item':{
                    'ID_order':result[0],
                    'ID_product':result[5],
                    'name':result[6],
                    'price':result[7],
                    'amount':result[8],
                    'discount':result[9],
                    'shared':result[10],
                    'comment':result[11],
                    'order_status':result[12],
                    'register':result[13]
                }
            }
        }

class SbOrdersUpdate(SbOrders):

    def update_order_status(self, status=0):
        try:
            self.cursor.execute("""UPDATE sb_orders SET order_status = ?, last_change = ? WHERE ID_order = ?""", (status, datetime.now(), self.orderId))
            self.conn.commit()
            return True
        except:
            return False