#!/usr/bin/python3
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
from flask import Flask, request, render_template, url_for, make_response, redirect
from sysbar.lib.client import SbWClient
from sysbar.core.tables.tables import SbTables
from sysbar.core.products.products import SbWProducts
from sysbar.core.products.category import SbCategory
import json
app = Flask(__name__)

@app.route("/")
def index():
    table = request.cookies.get('client_table')
    if not table:
        return redirect(url_for('table'))
    if not request.cookies.get('client_phone'):
        return redirect(url_for('login'))
    data = SbCategory().get_categories()
    return render_template('pt-br/index.html', data=data), 200

@app.route("/category/", methods=['GET'])
def category():
    cId = request.args.get('c')
    name = request.args.get('name')
    result = SbWProducts().get_products_for_category(cId)
    return render_template('pt-br/menu.html', category=name, cId=cId, data=result), 200

@app.route("/product/", methods=['GET'])
def product():
    pId = request.args.get('p')
    name = request.args.get('category')
    cId = request.args.get('c')
    result = SbWProducts(pId).get_product_simple_info()
    return render_template("pt-br/produto.html", category=name, cId=cId, data=result), 200

@app.route("/profile/")
def profile():
    return render_template('pt-br/perfil.html'), 200

@app.route("/table/")
def table():
    return render_template('pt-br/mesa.html'), 200

@app.route("/carrinho/")
def carrinho():
    return render_template('pt-br/carrinho.html'), 200

@app.route("/login/")
def login():
    table = request.cookies.get('client_table')
    if not table:
        return redirect(url_for('table'))
    
    return render_template('pt-br/entrar.html'), 200

@app.route("/signup/")
def signup():
    table = request.cookies.get('client_table')
    if not table:
        return redirect(url_for('table'))
    
    return render_template('pt-br/cadastro.html'), 200

@app.route("/status/")
def status():
    return '{"version":"0.1", "status":"active"}', 200, {"Content-Type": "application/json"}

@app.route("/about/")
def about():
    return render_template('pt-br/sobre.html'), 200

@app.route("/api/set_table/", methods=['GET'])
def api_set_table():
    table = request.args.get('table')
    if not table:
        return '{"rStatus":0}', 200, {"Content-Type": "application/json"}
    if not table.isdigit():
        return '{"rStatus":0}', 200, {"Content-Type": "application/json"}
    result = SbTables()
    if not result.search_table(table):
        json = '{"rStatus":0}'
        return make_response(json, 200, {"Content-Type": "application/json"})
    json = '{"rStatus":1}'
    resp = make_response(json, 200, {"Content-Type": "application/json"})
    resp.set_cookie('client_table', table)
    return resp

@app.route("/api/new_client/", methods=['GET'])
def api_new_client():
    phone = request.args.get('phone')
    name = request.args.get('name')
    pin = request.args.get('pin')
    if not phone or not name or not pin:
        return json.dumps({'rStatus':11}), 200, {"Content-Type": "application/json"}
    new = SbWClient()
    rNew = new.new_account(name, phone, pin)
    return json.dumps(rNew), 200, {"Content-Type": "application/json"}

@app.route("/api/login/", methods=['GET'])
def api_login():
    phone = request.args.get('phone')
    pin = request.args.get('pin')
    table = request.cookies.get('client_table')
    if not phone or not pin or not table:
        return json.dumps({'rStatus':11}), 200, {"Content-Type": "application/json"}
    print("{}- {} - {}".format(phone, pin, table))
    login = SbWClient()
    result = login.login(phone, pin, table)
    if result['rStatus']==1:
        resp = make_response(json.dumps({"rStatus":1}), 200, {"Content-Type": "application/json"})
        resp.set_cookie('client_phone', phone)
        resp.set_cookie('client_id', str(result['user']['id']))
        resp.set_cookie('client_name', result['user']['name'])
        return resp
    else:
        return json.dumps(result), 200, {"Content-Type": "application/json"}

if __name__=="__main__":
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=8080)
