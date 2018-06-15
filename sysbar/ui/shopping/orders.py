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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import json
from sysbar.ui.dialog import UiDialog
from sysbar.ui.products.products import UiInfoProduct
from sysbar.ui.client import UiCustomerInfo
from sysbar.core.shopping.orders import SbOrders, SbOrdersUpdate
from sysbar.core.tools.date import SbDateFormat
class UiInfoOrder(Gtk.Window):
    
    def __init__(self, orderId):
        Gtk.Window.__init__(self, window_position="center")
        self.set_resizable(False)

        data = SbOrders(orderId).get_order_info()
        if data['rStatus']==0:
            UiDialog("Não encontrado!", "Não encontramos a ordem selecionada.")
            return self.destroy()
        
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        self.set_title("Informações da ordem (ID: {})".format(data['data']['item']['ID_order']))

        # Aceitar ordem
        button = Gtk.Button(label="ENTREGAR PEDIDO", height_request=60)
        button.connect("clicked", self.update_status, [data['data']['item']['ID_order'], data['data']['ID_comanda'], data['data']['ID_table'], data['data']['client_name']])
        grid.attach(button, 1, 1, 2, 1)

        button = Gtk.Button(label="IGNORAR", height_request=60)
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 4, 1, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10)
        grid.attach(separator, 1, 2, 5, 1)

        # Título
        label = Gtk.Label(margin_bottom=20, halign="start")
        label.set_markup("<span size='20000'>Informações da ordem (ID: {})</span>".format(data['data']['item']['ID_order']))
        grid.attach(label, 1, 3, 5, 1)

        # Lado esquerdo
        # Nome do produto
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Produto:</span> <span color='blue' size='12000'>{}</span> (ID: {})".format(data['data']['item']['name'], data['data']['item']['ID_product']))
        grid.attach(label, 1, 4, 2, 1)

        button = Gtk.Button(label="Informações do produto")
        button.connect("clicked", self.show_product, data['data']['item']['ID_product'])
        grid.attach(button, 1, 5, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 1, 6, 2, 1)

        # Ordem compartilhada
        shared = json.loads(data['data']['item']['shared'])
        label = Gtk.Label(halign="start")
        if shared['number']==1:
            label.set_markup("<span font='bold'>Este pedido será pago por:</span> <span color='blue' size='12000'>{}</span> pessoa".format(shared['number']))
            grid.attach(label, 1, 7, 2, 1)

            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            grid.attach(separator, 1, 8, 2, 1)

            # Preço do produto
            label = Gtk.Label(halign="start")
            label.set_markup("<span font='bold'>Valor total:</span> <span color='blue' size='12000'>R$ {}</span> por <span color='blue' size='12000'>{}x</span>".format(str(data['data']['item']['price']).replace(".", ","), data['data']['item']['amount']))
            grid.attach(label, 1, 9, 2, 1)
            
            label = Gtk.Label(halign="start")
            label.set_markup("<span font='bold'>Desconto:</span> <span color='blue' size='12000'>R$ {}</span>".format(str(data['data']['item']['discount']).replace(".", ",")))
            grid.attach(label, 1, 10, 2, 1)
        else:
            label.set_markup("<span font='bold'>Este pedido será pago por:</span> <span color='blue' size='12000'>{}</span> pessoas".format(shared['number']))
            grid.attach(label, 1, 7, 1, 1)

            button = Gtk.Button(label="Origem")
            button.connect("clicked", self.show_customer, shared['source'])
            grid.attach(button, 2, 7, 1, 1)

            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            grid.attach(separator, 1, 8, 2, 1)

            # Preço do produto
            label = Gtk.Label(halign="start")
            label.set_markup("<span font='bold'>Valor total:</span> <span color='blue' size='12000'>R$ {}</span> por <span color='blue' size='12000'>{}x</span>".format(str(data['data']['item']['price']*shared['number']).replace(".", ","), data['data']['item']['amount']))
            grid.attach(label, 1, 9, 2, 1)
            
            label = Gtk.Label(halign="start")
            label.set_markup("<span font='bold'>Desconto:</span> <span color='blue' size='12000'>R$ {}</span>".format(str(data['data']['item']['discount']).replace(".", ",")))
            grid.attach(label, 1, 10, 2, 1)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 1, 11, 2, 1)

        # Comentário sobre o pedido
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Comentário:</span>")

        scrolledwindow = Gtk.ScrolledWindow(width_request=200, height_request=50)

        description = Gtk.TextView(width_request=200, height_request=50)
        description.set_editable(False)
        description.set_cursor_visible(False)
        text = description.get_buffer()
        if data['data']['item']['comment']:
            text.set_text(str(data['data']['item']['comment']))
        
        scrolledwindow.add(description)
        grid.attach(label, 1, 12, 2, 1)
        grid.attach(scrolledwindow, 1, 13, 2, 5)

        # Meio
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(separator, 3, 4, 1, 16)

        # Lado direito
        # ID da comanda
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold' size='14000'>COMANDA:</span> <span color='blue' size='14000'>{}</span>".format(data['data']['ID_comanda']))
        grid.attach(label, 4, 4, 2, 1)
        
        # ID da mesa
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold' size='14000'>MESA:</span> <span color='blue' size='14000'>{}</span>".format(data['data']['ID_table']))
        grid.attach(label, 4, 5, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 4, 6, 2, 1)

        # Nome do cliente
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Cliente:</span> <span color='blue' size='12000'>{}</span>".format(data['data']['client_name']))
        grid.attach(label, 4, 7, 2, 1)

        button = Gtk.Button(label="Informações sobre o cliente")
        button.connect("clicked", self.show_customer, data['data']['ID_client'])
        grid.attach(button, 4, 8, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 4, 9, 2, 1)

        # Registrado
        label = Gtk.Label()
        label.set_markup("<span font='bold'>Data do pedido:</span> {}".format(SbDateFormat(data['data']['item']['register'][:-7]).diff_passed_to_current()))
        grid.attach(label, 4, 10, 2, 1)
    
    def update_status(self, widget, data):
        if SbOrdersUpdate(data[0]).update_order_status():
            win = UiSuccessOrder(data)
            win.show_all()
            return self.destroy()
        return UiDialog('aa', 'aa')
    
    def show_product(self, widget, data):
        win = UiInfoProduct(data)
        win.show_all()
    
    def show_customer(self, widget, data):
        win = UiCustomerInfo(data, True)
        win.show_all()
    
    def destroy_window(self, widget):
        self.destroy()

class UiSuccessOrder(Gtk.Window):

    def __init__(self, data):
        Gtk.Window.__init__(self, window_position="center")
        self.set_resizable(False)
        
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(20)
        grid.set_column_spacing(20)
        self.add(grid)

        # self.set_title("Informações da ordem (ID: {})".format(data['data']['item']['ID_order']))

        # Títulos
        self.set_title("Entregue o pedido - ID: {}".format(data[0]))
        label = Gtk.Label(margin_bottom=20, halign="start")
        label.set_markup("<span font='bold' color='#c6262e' size='26000'>ENTREGUE O PEDIDO!</span>")
        grid.attach(label, 1, 1, 2, 1)

        # Mesa
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold' color='#3689e6' size='18000'>MESA: <span color='#0d52bf'>{}</span></span>".format(data[2]))
        grid.attach(label, 1, 2, 1, 1)

        # Comanda
        label = Gtk.Label(halign="end")
        label.set_markup("<span font='bold' color='#3689e6' size='18000'>COMANDA: <span color='#0d52bf'>{}</span></span>".format(data[1]))
        grid.attach(label, 2, 2, 1, 1)

        # Cliente
        label = Gtk.Label(halign="center")
        label.set_markup("<span font='bold' color='#68b723' size='19000'>PARA: <span color='#3a9104'>{}</span></span>".format(data[3].upper()))
        grid.attach(label, 1, 3, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10)
        grid.attach(separator, 1, 4, 2, 1)

        # Fechar
        button = Gtk.Button(label="Fechar", height_request=40)
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 1, 5, 1, 1)
        
        # Printer
        button = Gtk.Button(label="Imprimir", height_request=40)
        button.connect("clicked", self.printer)
        grid.attach(button, 2, 5, 1, 1)
    
    def printer(self, widget, data=None):
        pass
    
    def destroy_window(self, widget):
        return self.destroy()