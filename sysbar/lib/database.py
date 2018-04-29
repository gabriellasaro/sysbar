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
class DataBase():
    def creat_db_users(self):
        conn = sqlite3.connect('/home/gabriel/.system-bar/database/users.db')
        cursor = conn.cursor()
        cursor.execute("""
		CREATE TABLE `sb_users` (
			`ID_user`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			`username`	TEXT NOT NULL UNIQUE,
			`user_pin`	TEXT NOT NULL,
			`user_nicename`	TEXT NOT NULL,
			`user_phone`	TEXT,
			`user_email`	TEXT,
			`user_birthday`	NUMERIC NOT NULL,
			`user_address`	TEXT DEFAULT '{"district": "", "nation": "Brasil", "state": "Espírito Santo", "house": "SN", "city": "", "CEP": "", "street": "", "complement": ""}',
			`user_level`	INTEGER NOT NULL DEFAULT 1,
			`user_status`	INTEGER NOT NULL DEFAULT 1,
			`user_register`	TEXT NOT NULL
		);
        """)
        cursor.execute("""
		CREATE TABLE `sb_sessions` (
			`ID_session`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			`username`	TEXT NOT NULL,
			`computer_name`	TEXT NOT NULL,
			`register`	TEXT NOT NULL
		);
        """)
        conn.close()
    
    def creat_db_sysbar(self):
        conn = sqlite3.connect('/home/gabriel/.system-bar/database/sysbar.db')
        cursor = conn.cursor()
        cursor.execute("""
CREATE TABLE `sba_billing` (
	`IDA_billing`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`total_money`	REAL DEFAULT 0,
	`received`	REAL DEFAULT 0,
	`pending`	REAL DEFAULT 0,
	`credit`	REAL DEFAULT 0,
	`number_sales`	INTEGER DEFAULT 0,
	`month`	TEXT,
	`register`	TEXT
);
        """)
        cursor.execute("""
CREATE TABLE `sba_customer_product` (
	`IDA_client_p`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ID_client`	INTEGER NOT NULL,
	`ID_product`	INTEGER NOT NULL,
	`number_sales`	INTEGER DEFAULT 0,
	`month`	TEXT,
	`register`	TEXT
);
        """)
        cursor.execute("""
CREATE TABLE `sba_product` (
	`IDA_product`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ID_product`	INTEGER NOT NULL,
	`price`	REAL,
	`number_sales`	INTEGER NOT NULL DEFAULT 0,
	`order_shared`	INTEGER DEFAULT 0,
	`month`	TEXT NOT NULL,
	`register`	TEXT
);
        """)
        cursor.execute("""
CREATE TABLE `sba_tables` (
	`IDA_tables`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ID_table`	INTEGER,
	`price`	REAL DEFAULT 0,
	`number_people`	INTEGER,
	`usage_number`	INTEGER DEFAULT 0,
	`month`	TEXT,
	`register`	TEXT
);	
        """)
        cursor.execute("""
CREATE TABLE `sb_list_categories` (
	`ID_category`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`category`	TEXT,
	`register`	TEXT
);
        """)
		cursor.execute("""
CREATE TABLE `sb_tables` (
	`ID_table`	INTEGER NOT NULL UNIQUE,
	`table_price`	REAL NOT NULL DEFAULT 0,
	`busy_table`	INTEGER DEFAULT 0,
	`table_capacity`	INTEGER DEFAULT 2,
	`register`	TEXT
);
		""")
        cursor.execute("""
CREATE TABLE `sb_client` (
	`ID_client`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`client_phone`	TEXT NOT NULL UNIQUE,
	`client_pin`	TEXT NOT NULL,
	`client_name`	TEXT NOT NULL,
	`client_cpf`	INTEGER DEFAULT NULL,
	`client_birthday`	NUMERIC,
	`client_credit`	REAL NOT NULL DEFAULT 0,
	`last_purchase`	TEXT DEFAULT NULL,
	`register`	TEXT NOT NULL,
	`last_change`	TEXT DEFAULT NULL
);
        """)
        cursor.execute("""
CREATE TABLE `sb_delivery_address` (
	`ID_address`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ID_client`	INTEGER NOT NULL,
	`CEP`	TEXT,
	`house_number`	TEXT NOT NULL DEFAULT 'SN',
	`complement`	TEXT DEFAULT NULL,
	`street`	TEXT NOT NULL,
	`district`	TEXT NOT NULL,
	`city`	TEXT NOT NULL,
	`state`	TEXT NOT NULL DEFAULT 'Espírito Santo',
	`nation`	TEXT NOT NULL DEFAULT 'Brasil',
	`comment`	TEXT,
	`usage`	INTEGER DEFAULT 0,
	`address_register`	TEXT NOT NULL
);
        """)
		cursor.execute("""
CREATE TABLE `sb_list_comandas` (
	`ID_comanda`	INTEGER NOT NULL,
	`ID_client`	INTEGER NOT NULL,
	`ID_table`	INTEGER DEFAULT 0,
	`deliver`	INTEGER NOT NULL DEFAULT 0,
	`ID_address`	INTEGER DEFAULT 0,
	`status`	TEXT DEFAULT 'open',
	`register`	TEXT NOT NULL
);
		""")
        cursor.execute("""
CREATE TABLE `sb_orders` (
	`ID_order`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ID_comanda`	INTEGER NOT NULL,
	`ID_client`	INTEGER,
	`ID_product`	INTEGER NOT NULL,
	`price`	REAL,
	`amount`	INTEGER DEFAULT 1,
	`discount`	INTEGER DEFAULT 0,
	`order_shared`	TEXT DEFAULT 1,
	`order_status`	INTEGER DEFAULT 1,
	`register`	TEXT
);
        """)
        cursor.execute("""
CREATE TABLE `sb_product` (
	`ID_product`	INTEGER NOT NULL UNIQUE,
	`barcode`	INTEGER,
	`product_name`	TEXT NOT NULL,
	`product_img`	TEXT NOT NULL,
	`product_description`	TEXT NOT NULL,
	`product_price`	REAL NOT NULL,
	`product_cost`	REAL NOT NULL DEFAULT 0,
	`product_discount`	INTEGER DEFAULT 0,
	`product_stock`	INTEGER NOT NULL DEFAULT 0,
	`stock_status`	INTEGER NOT NULL DEFAULT 0,
	`register`	TEXT,
	`last_change`	TEXT DEFAULT NULL,
	PRIMARY KEY(ID_product)
);
        """)
        cursor.execute("""
CREATE TABLE `sb_meta_product` (
	`ID_product`	INTEGER NOT NULL UNIQUE,
	`ID_category`	INTEGER NOT NULL,
	`virtual_menu`	INTEGER DEFAULT 1,
	`special_request`	INTEGER DEFAULT 0,
	`delivery`	INTEGER DEFAULT 0,
	`unity`	TEXT NOT NULL,
	`amount`	REAL NOT NULL,
	`people_served`	INTEGER DEFAULT 0,
	`status`	INTEGER DEFAULT 0,
	`register`	TEXT,
	PRIMARY KEY(ID_product)
);
        """)
        cursor.execute("""
CREATE TABLE `sb_special_request` (
	`ID_specialrequest`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ID_product`	INTEGER NOT NULL,
	`ID_client`	INTEGER NOT NULL,
	`description`	TEXT NOT NULL,
	`sr_price`	REAL NOT NULL DEFAULT 0,
	`sr_type`	TEXT NOT NULL DEFAULT 'remove',
	`status_sr`	INTEGER DEFAULT 0,
	`register`	TEXT NOT NULL,
	`sr_last_change`	TEXT DEFAULT NULL
);
        """)
        conn.close()