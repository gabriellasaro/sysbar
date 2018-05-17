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
import requests, json
from sysbar.ui.dialog import UiDialog
from sysbar.lib.client import SbClient, SbDClient

class UiCustomerList(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Lista de clientes - SysBar", window_position="center")
        self.set_default_size(800, 600)
        grid = Gtk.Grid(margin=20)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Clientes:</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Lista
        self.liststore = Gtk.ListStore(int, str, str, float)
        # ID - PHONE - NAME - CREDIT
        data = SbClient()
        rData = data.get_customer_list()
        if rData['rStatus']==1:
            for client in rData['data']:
                self.liststore.append([client[0], client[1], client[2], client[3]])
        
        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        treeview.set_search_column(2)
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.connect("row-activated", self.on_row_activated)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(treeview)
        grid.attach(scrolledwindow, 1, 2, 2, 1)

        cellrenderertext = Gtk.CellRendererText()
        
        treeviewcolumn = Gtk.TreeViewColumn("ID")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Telefone")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Nome")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 2)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Crédito")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 3)
        treeview.append_column(treeviewcolumn)
        
        button = Gtk.Button(label="Novo cliente", margin_top=10, height_request=40, halign="start")
        button.connect("clicked", self.show_new_client)
        grid.attach(button, 1, 3, 1, 1)

        button = Gtk.Button(label="Atualizar", margin_top=10, height_request=40, halign="end")
        button.connect("clicked", self.update_list)
        grid.attach(button, 2, 3, 1, 1)
    
    def update_list(self, widget):
        self.liststore.clear()
        # ID - PHONE - NAME - CREDIT
        data = SbClient()
        rData = data.get_customer_list()
        if rData['rStatus']==1:
            for client in rData['data']:
                self.liststore.append([client[0], client[1], client[2], client[3]])
    
    def on_row_activated(self, widget, treepath, text):
        win = UiCustomerInfo(self.liststore[treepath][1])
        win.show_all()
    
    def show_new_client(self, widget):
        win = UiNewCustomer()
        win.show_all()

class UiCustomerInfo(Gtk.Window):

    def __init__(self, customerPhone):
        Gtk.Window.__init__(self, title="Informações sobre o cliente", window_position="center")
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        client = SbClient()
        dataClient = client.get_customer_information(customerPhone)
        if dataClient['rStatus']==0:
            self.set_resizable(False)

            label = Gtk.Label()
            label.set_markup("<span size='20000' color='red'>Não encontramos o cliente!</span>")
            grid.attach(label, 1, 1, 1, 1)

            button = Gtk.Button(margin_top=10, width_request=100, height_request=40, halign="end")
            button.set_label("Fechar")
            button.connect("clicked", self.destroy_window)
            grid.attach(button, 1, 2, 1, 1)
        else:
            self.set_default_size(900, 550)
            # Título
            label = Gtk.Label(margin_bottom=30, halign="start")
            label.set_markup("<span size='20000'>Informações do cliente</span>")
            grid.attach(label, 1, 1, 7, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("<span size='15000'>Nome: <span color='blue'>{}</span></span>".format(dataClient['data'][2]))
            grid.attach(label, 1, 2, 7, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("Telefone: <span color='blue'>{}</span>".format(dataClient['data'][1]))
            grid.attach(label, 1, 3, 7, 1)

            label = Gtk.Label(halign="start")
            if dataClient['data'][3]==None or len(dataClient['data'][3])==0:
                label.set_markup("Aniversário: <span color='red'>Não informado.</span>")
            else:
                label.set_markup("Aniversário: <span color='blue'>{}</span>".format(dataClient['data'][3]))
            grid.attach(label, 1, 5, 7, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("Crédito: <span color='blue'>{}</span>".format(dataClient['data'][4]))
            grid.attach(label, 1, 6, 7, 1)
        
            label = Gtk.Label(halign="start")
            if dataClient['data'][5] == None:
                label.set_markup("Última compra: <span color='blue'>Nunca comprou</span>")                
            else:
                label.set_markup("Última compra: <span color='blue'>{}</span>".format(dataClient['data'][5]))
            grid.attach(label, 1, 7, 7, 1)

            # Lista
            self.liststore = Gtk.ListStore(int, str, str, str, str, str, str, str, str, int)
            client.set_customer_id(dataClient['data'][0])
            rAddress = client.get_customer_address()
            # ID - CEP - HOUSE NUMBER - STREET - DISTRICT - COMPLEMENT - CITY - STATE - COMMENT - USAGE
            if rAddress['rStatus']==1:
                for address in rAddress['data']:
                    self.liststore.append([address[0], address[1], address[2], address[3], address[4], address[5], address[6], address[7], address[8], address[9]])
        
            treeview = Gtk.TreeView()
            treeview.set_model(self.liststore)
            treeview.set_search_column(2)
            treeview.set_vexpand(True)
            treeview.set_hexpand(True)
            treeview.connect("row-activated", self.on_row_activated)

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.add(treeview)
            grid.attach(scrolledwindow, 1, 8, 7, 1)

            cellrenderertext = Gtk.CellRendererText()

            treeviewcolumn = Gtk.TreeViewColumn("ID")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("CEP")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("Nº. casa")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 2)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("Logradouro")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 3)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("Complemento")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 4)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("Bairro")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 5)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("Cidade")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 6)
            treeview.append_column(treeviewcolumn)
    
            treeviewcolumn = Gtk.TreeViewColumn("Estado")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 7)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("Comentário")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 8)
            treeview.append_column(treeviewcolumn)

            treeviewcolumn = Gtk.TreeViewColumn("Usado")
            # treeviewcolumn.set_spacing(10)
            treeviewcolumn.set_resizable(True)
            treeviewcolumn.pack_start(cellrenderertext, False)
            treeviewcolumn.add_attribute(cellrenderertext, "text", 9)
            treeview.append_column(treeviewcolumn)

            button = Gtk.Button(height_request=40)
            button.set_label("Novo endereço")
            button.connect("clicked", self.show_new_address, dataClient['data'][0])
            grid.attach(button, 1, 9, 1, 1)

            button = Gtk.Button()
            button.set_label("Alterar nome")
            button.connect("clicked", self.show_update_name, dataClient['data'][0], dataClient['data'][2])
            grid.attach(button, 2, 9, 1, 1)

            button = Gtk.Button()
            button.set_label("Alterar telefone")
            button.connect("clicked", self.show_change_phone, dataClient['data'][0], dataClient['data'][1])
            grid.attach(button, 3, 9, 1, 1)

            button = Gtk.Button()
            button.set_label("Alterar PIN")
            button.connect("clicked", self.show_new_pin, dataClient['data'][0])
            grid.attach(button, 4, 9, 1, 1)

            button = Gtk.Button()
            button.set_label("Atualizar lista")
            button.connect("clicked", self.update_list, dataClient['data'][0])
            grid.attach(button, 5, 9, 1, 1)

            button = Gtk.Button()
            button.set_label("Atualizar")
            button.connect("clicked", self.update_window, customerPhone)
            grid.attach(button, 6, 9, 1, 1)

            button = Gtk.Button()
            button.set_label("Fechar")
            button.connect("clicked", self.destroy_window)
            grid.attach(button, 7, 9, 1, 1)
    
    def update_list(self, widget, clientId):
        self.liststore.clear()
        client = SbClient()
        client.set_customer_id(clientId)
        rAddress = client.get_customer_address()
        # ID - CEP - HOUSE NUMBER - STREET - DISTRICT - COMPLEMENT - CITY - STATE - COMMENT - USAGE
        if rAddress['rStatus']==1:
            for address in rAddress['data']:
                self.liststore.append([address[0], address[1], address[2], address[3], address[4], address[5], address[6], address[7], address[8], address[9]])

    def on_row_activated(self, widget, treepath, text):
        win = UiDeleteAddress(self.liststore[treepath][0])
        win.show_all()
    
    def show_new_address(self, widget, clientId):
        win = UiNewAddress(clientId)
        win.show_all()
    
    def show_new_pin(self, widget, clientId):
        win = UiNewPin(clientId)
        win.show_all()
    
    def show_update_name(self, widget, clientId, name):
        win = UiUpdateClientName(clientId, name)
        win.show_all()
    
    def show_change_phone(self, widget, clientId, number):
        win = UiChangePhone(clientId, number)
        win.show_all()
    
    def update_window(self, widget, phone):
        self.destroy()
        win = UiCustomerInfo(phone)
        win.show_all()
    
    def destroy_window(self, widget):
        return self.destroy()

class UiNewCustomer(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Cadastro de cliente", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=20, halign="start")
        label.set_markup("<span size='20000'>Cadastro de cliente</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nome
        label = Gtk.Label(halign="start")
        label.set_markup("Nome completo:<span color='red'>*</span>")
        self.name = Gtk.Entry(max_length=120)
        grid.attach(label, 1, 2, 3, 1)
        grid.attach(self.name, 1, 3, 3, 1)

        # Telefone
        label = Gtk.Label(halign="start")
        label.set_markup("Telefone:<span color='red'>*</span>")
        self.phone = Gtk.Entry(max_length=12)
        self.phone.set_input_purpose(Gtk.InputPurpose.PHONE)
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.phone, 1, 5, 1, 1)

        # PIN
        label = Gtk.Label(halign="start")
        label.set_markup("PIN:<span color='red'>*</span> (4 números)")
        self.pin = Gtk.Entry(max_length=4)
        grid.attach(label, 2, 4, 1, 1)
        grid.attach(self.pin, 2, 5, 1, 1)

        # Aniversário
        label = Gtk.Label(halign="start")
        label.set_label("Aniversário:")
        self.birthday = Gtk.Entry(max_length=10)
        grid.attach(label, 3, 4, 1, 1)
        grid.attach(self.birthday, 3, 5, 1, 1)

        # Info
        label = Gtk.Label(margin_top=10)
        label.set_markup("No campo telefone insira somente números, sempre com o DDD incluso.")
        grid.attach(label, 1, 6, 3, 1)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 7, 3, 1)

        # Enviar
        submit = Gtk.Button(label="Enviar", height_request=40)
        submit.connect("clicked", self.submit_client)
        grid.attach(submit, 1, 8, 3, 1)

    def submit_client(self, widget):
        phone = self.phone.get_text().strip()
        client = SbDClient()
        rData = client.new(self.name.get_text(), phone, self.pin.get_text(), self.birthday.get_text())
        if rData['rStatus']==11:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        elif rData['rStatus']==9:
            return UiDialog("Erro!", "Cliente já cadastrado.")            
        elif rData['rStatus']==0:
            self.destroy()
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")
        else:
            self.destroy()
            data = client.get_customer_id_by_phone(phone)
            if data['rStatus']==1:
                win = UiNewAddress(data['data'])
                win.show_all()

class UiNewPin(Gtk.Window):

    def __init__(self, clientId):
        Gtk.Window.__init__(self, title="Alterar PIN", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Alterar PIN</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nova PIN
        label = Gtk.Label(halign="start")
        label.set_label("Novo PIN: (4 números)")
        self.newPin = Gtk.Entry(max_length=4)
        self.newPin.set_input_purpose(Gtk.InputPurpose.NUMBER)
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.newPin, 1, 5, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 8, 1, 1)

        # Enviar
        button = Gtk.Button(label="Atualizar", height_request=40)
        button.connect("clicked", self.update_pin, clientId)
        grid.attach(button, 1, 9, 1, 1)
    
    def update_pin(self, widget, clientId):
        pin = self.newPin.get_text()
        if len(str(pin))<4 or len(str(pin))>4:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        self.destroy()
        submit = SbDClient(clientId)
        if not submit.update_pin(pin):
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")

class UiUpdateClientName(Gtk.Window):

    def __init__(self, clientId, name):
        Gtk.Window.__init__(self, title="Alterar Nome", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30)
        label.set_markup("<span size='20000'>Alterar nome do cliente</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nome
        label = Gtk.Label(label="Nome completo:")
        self.name = Gtk.Entry(width_request=350)
        self.name.set_text(name)
        self.name.connect("activate", self.update_name, clientId)
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.name, 1, 3, 1, 1)

        # Enviar
        button = Gtk.Button(label="Atualizar", height_request=40)
        button.connect("clicked", self.update_name, clientId)
        grid.attach(button, 1, 4, 1, 1)
    
    def update_name(self, widget, clientId):
        name = self.name.get_text()
        submit = SbClient(clientId)
        self.destroy()
        if not submit.change_name(name):
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")

class UiChangePhone(Gtk.Window):

    def __init__(self, clientId, number):
        Gtk.Window.__init__(self, title="Alterar número do telefone", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30)
        label.set_markup("<span size='20000'>Alterar número do telefone</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Telefone
        label = Gtk.Label(label="Novo número: (somente números)")
        self.number = Gtk.Entry(max_length=12, width_request=200)
        self.number.set_text(number)
        self.number.connect("activate", self.update_number, clientId)
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.number, 1, 3, 1, 1)

        # Enviar
        button = Gtk.Button(label="Atualizar", height_request=40)
        button.connect("clicked", self.update_number, clientId)
        grid.attach(button, 1, 4, 1, 1)

    def update_number(self, widget, clientId):
        submit = SbClient(clientId)
        result = submit.change_phone_number(self.number.get_text())
        if result['rStatus']==11:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        elif result['rStatus']==9:
            return UiDialog("Erro!", "Não é possível atulizar, o número já está cadastrado.")
        elif result['rStatus']==0:
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")
        else:
            return self.destroy()

class UiNewAddress(Gtk.Window):

    def __init__(self, clientId):
        Gtk.Window.__init__(self, title="Novo endereço", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Novo endereço</span>")
        grid.attach(label, 1, 1, 1, 1)

        # CEP
        label = Gtk.Label(halign="start")
        label.set_label("CEP:")
        self.cep = Gtk.Entry(max_length=10)
        self.cep.set_input_purpose(Gtk.InputPurpose.NUMBER)
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.cep, 1, 3, 1, 1)

        # Buscar CEP
        button = Gtk.Button(label="Buscar CEP")
        button.connect("clicked", self.search_cep)
        grid.attach(button, 2, 3, 1, 1)

        # Rua
        label = Gtk.Label(halign="start")
        label.set_markup("Rua<span color='red'>*</span>:")
        self.street = Gtk.Entry(max_length=120)
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.street, 1, 5, 3, 1)

        # Complemento
        label = Gtk.Label(halign="start")
        label.set_label("Complemento:")
        self.complement = Gtk.Entry(width_request=300)
        grid.attach(label, 1, 6, 1, 1)
        grid.attach(self.complement, 1, 7, 2, 1)

        # Número da casa
        label = Gtk.Label(halign="start")
        label.set_label("Número da casa:")
        self.house = Gtk.Entry(max_length=5)
        self.house.set_input_purpose(Gtk.InputPurpose.NUMBER)
        grid.attach(label, 3, 6, 1, 1)
        grid.attach(self.house, 3, 7, 1, 1)

        # Bairro
        label = Gtk.Label(halign="start")
        label.set_markup("Bairro<span color='red'>*</span>:")
        self.bairro = Gtk.Entry(max_length=120)
        grid.attach(label, 1, 8, 1, 1)
        grid.attach(self.bairro, 1, 9, 2, 1)

        # Cidade
        label = Gtk.Label(halign="start")
        label.set_markup("Cidade<span color='red'>*</span>:")
        self.city = Gtk.Entry(max_length=120)
        grid.attach(label, 3, 8, 1, 1)
        grid.attach(self.city, 3, 9, 1, 1)

        # Estado
        label = Gtk.Label(halign="start")
        label.set_label("Estado:")

        liststore = Gtk.ListStore(str)

        listStates = [
            "Acre",
            "Alagoas",
            "Amapá",
            "Amazonas",
            "Bahia",
            "Ceará",
            "Distrito Federal",
            "Espírito Santo",
            "Goiás",
            "Maranhão",
            "Mato Grosso",
            "Mato Grosso do Sul",
            "Minas Gerais",
            "Pará",
            "Paraíba",
            "Paraná",
            "Pernambuco",
            "Piauí",
            "Rio de Janeiro",
            "Rio Grande do Norte",
            "Rio Grande do Sul",
            "Rondônia",
            "Roraima",
            "Santa Catarina",
            "São Paulo",
            "Sergipe",
            "Tocantins"
        ]
        for item in listStates:
            liststore.append([item])
        
        entrycompletion = Gtk.EntryCompletion()
        entrycompletion.set_model(liststore)
        entrycompletion.set_text_column(0)
        entrycompletion.set_inline_completion(True)

        self.state = Gtk.Entry(max_length=120)
        self.state.set_completion(entrycompletion)
        self.state.set_text("ES")
        grid.attach(label, 1, 10, 1, 1)
        grid.attach(self.state, 1, 11, 1, 1)

        # Comentário
        label = Gtk.Label(halign="start")
        label.set_label("Comentário:")
        self.comment = Gtk.Entry()
        grid.attach(label, 2, 10, 1, 1)
        grid.attach(self.comment, 2, 11, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=20, margin_bottom=20)
        grid.attach(separator, 1, 12, 3, 1)

        # Enviar
        submit = Gtk.Button(label="Enviar", height_request=40)
        submit.connect("clicked", self.submit_address, clientId)
        grid.attach(submit, 1, 13, 2, 1)

        # Cancelar
        button = Gtk.Button(label="Fechar", height_request=40)
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 3, 13, 1, 1)
        
    def destroy_window(self, widget):
        return self.destroy()
    
    def submit_address(self, widget, clientId):
        house = self.house.get_text().strip()
        if len(house)==0:
            house = "SN"
        if len(self.street.get_text())==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if len(self.bairro.get_text())==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if len(self.city.get_text())==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        insert = SbDClient(clientId)
        result = insert.new_address(self.cep.get_text(), house, self.street.get_text(), self.complement.get_text(), self.bairro.get_text(), self.city.get_text(), self.state.get_text(), self.comment.get_text())
        self.destroy()
        if not result:
            UiDialog("Erro ao enviar", "Erro ao inserir as informações no banco de dados.")
    
    def search_cep(self, widget):
        cep = self.cep.get_text().replace("-", "")
        if len(cep)==8:
            request = requests.get("https://viacep.com.br/ws/{}/json/".format(cep))
            if request.status_code==200:
                data = request.json()
                self.street.set_text(data.get('logradouro', ''))
                self.complement.set_text(data.get('complemento', ''))
                self.bairro.set_text(data.get('bairro', ''))
                self.city.set_text(data.get('localidade', ''))
                self.state.set_text(data.get('uf', ''))

class UiDeleteAddress(Gtk.Window):

    def __init__(self, addressId):
        Gtk.Window.__init__(self, title="Deletar Endereço?", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(30)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(halign="center")
        label.set_markup("<span size='20000'>Deseja deletar o endereço?</span>")
        grid.attach(label, 1, 1, 2, 1)

        button = Gtk.Button(label="Não")
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 1, 2, 1, 1)

        button = Gtk.Button(label="Sim", height_request=40)
        button.connect("clicked", self.delete_address, addressId)
        grid.attach(button, 2, 2, 1, 1)
    
    def delete_address(self, widget, addressId):
        self.destroy()
        submit = SbDClient()
        if not submit.delete_address(addressId):
            return UiDialog("Erro", "Erro ao deletar endereço.")
    
    def destroy_window(self, widget):
        return self.destroy()