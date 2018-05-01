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
from gi.repository.GdkPixbuf import Pixbuf
import requests, json
from sysbar.ui.dialog import UiDialog
from sysbar.lib.user import SbUser, SbDUser
from sysbar.lib.validation import SbFormatString
from sysbar.lib.session import SbSession
class UiUserList(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Lista de usuários", window_position="center")
        self.set_default_size(800, 600)
        grid = Gtk.Grid(margin=20)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Usuários:</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Lista
        # ID - USERNAME - NAME - PHONE - LEVEL
        self.liststore = Gtk.ListStore(int, str, str, str, int)
        data = SbUser()
        rData = data.get_user_list()
        if rData['rStatus']==1:
            for user in rData['data']:
                self.liststore.append([user[0], user[1], user[2], user[3], user[4]])
        
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

        treeviewcolumn = Gtk.TreeViewColumn("username")
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

        treeviewcolumn = Gtk.TreeViewColumn("Telefone")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 3)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Nível de permissão")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 4)
        treeview.append_column(treeviewcolumn)

        button = Gtk.Button(label="Novo usuário", margin_top=10, height_request=40, halign="start")
        button.connect("clicked", self.show_new_client)
        grid.attach(button, 1, 3, 1, 1)

        button = Gtk.Button(label="Atualizar", margin_top=10, height_request=40, halign="end")
        button.connect("clicked", self.update_list)
        grid.attach(button, 2, 3, 1, 1)
    
    def update_list(self, widget):
        self.liststore.clear()
        data = SbUser()
        rData = data.get_user_list()
        if rData['rStatus']==1:
            for user in rData['data']:
                self.liststore.append([user[0], user[1], user[2], user[3], user[4]])
    
    def on_row_activated(self, widget, treepath, text):
        win = UiUserInfo(self.liststore[treepath][0])
        win.show_all()
    
    def show_new_client(self, widget):
        win = UiNewUser()
        win.show_all()

class UiUserInfo(Gtk.Window):

    def __init__(self, userId):
        Gtk.Window.__init__(self, title="Informações do usuário", window_position="center")

        user = SbUser(userId)
        data = user.get_user_info()

        if data['rStatus']==0:
            UiDialog('Atenção!', 'Não encontramos o usuário.')
            return self.destroy()
        
        self.set_resizable(False)

        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)
        
        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Informações</span>")
        grid.attach(label, 1, 1, 4, 1)

        # Informações
        label = Gtk.Label(halign="start")
        label.set_markup("Nome: <span color='blue'>{}</span>".format(data['data'][2]))
        grid.attach(label, 1, 2, 3, 1)
        
        label = Gtk.Label(halign="start")
        label.set_markup("Username: <span color='blue'>{}</span>".format(data['data'][1]))
        grid.attach(label, 1, 3, 3, 1)
        
        label = Gtk.Label(halign="start")
        label.set_markup("Telefone: <span color='blue'>{}</span>".format(data['data'][3]))
        grid.attach(label, 1, 4, 3, 1)
        
        label = Gtk.Label(halign="start")
        label.set_markup("E-mail: <span color='blue'>{}</span>".format(data['data'][4]))
        grid.attach(label, 1, 5, 3, 1)
        
        label = Gtk.Label(halign="start")
        date = SbFormatString()
        label.set_markup("Aniversário: <span color='blue'>{}</span>".format(date.format_date_for_string(data['data'][5])))
        grid.attach(label, 1, 6, 3, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(separator, 4, 2, 1, 5)

        # Endereço
        addr = json.loads(data['data'][6])
        
        label = Gtk.Label(halign="start")
        label.set_markup("Logradouro: <span color='blue'>{}</span>".format(addr['street']))
        grid.attach(label, 5, 2, 3, 1)
        
        label = Gtk.Label(halign="start")
        label.set_markup("Casa nº: <span color='blue'>{}</span>, compl.: <span color='blue'>{}</span>".format(addr['house'], addr['complement']))
        grid.attach(label, 5, 3, 3, 1)

        label = Gtk.Label(halign="start")
        label.set_markup("Bairro: <span color='blue'>{}</span>".format(addr['district']))
        grid.attach(label, 5, 4, 3, 1)

        label = Gtk.Label(halign="start")
        label.set_markup("Cidade: <span color='blue'>{}</span>".format(addr['city']))
        grid.attach(label, 5, 5, 3, 1)
        
        label = Gtk.Label(halign="start")
        label.set_markup("Estado: <span color='blue'>{} - {}</span>".format(addr['state'], addr['nation']))
        grid.attach(label, 5, 6, 3, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 7, 7, 1)

        # Título
        label = Gtk.Label(halign="start")
        label.set_label("Alterar informações:")
        grid.attach(label, 1, 8, 7, 1)

        # Novo grid
        grid2 = Gtk.Grid()
        grid2.set_column_spacing(10)
        grid2.set_row_spacing(10)
        grid.attach(grid2, 1, 9, 7, 1)

        # Botões
        button = Gtk.Button(width_request=100, height_request=40)
        button.set_label("Endereço")
        button.connect("clicked", self.show_new_address, data['data'][0])
        grid2.attach(button, 1, 1, 1, 1)
        
        button = Gtk.Button(width_request=100)
        button.set_label("Nome")
        button.connect("clicked", self.show_update_name, data['data'][0], data['data'][2])
        grid2.attach(button, 2, 1, 1, 1)
        
        button = Gtk.Button(width_request=100)
        button.set_label("Contato")
        button.connect("clicked", self.show_change_contacts, [data['data'][0], data['data'][3], data['data'][4]])
        grid2.attach(button, 3, 1, 1, 1)
        
        button = Gtk.Button(width_request=100)
        button.set_label("Permissão")
        button.connect("clicked", self.show_new_level, [data['data'][0], data['data'][7]])
        grid2.attach(button, 4, 1, 1, 1)

        button = Gtk.Button(width_request=100)
        button.set_label("PIN")
        button.connect("clicked", self.show_new_pin, [data['data'][0], data['data'][1], data['data'][7]])
        grid2.attach(button, 5, 1, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid2.attach(separator, 1, 2, 5, 1)

        label = Gtk.Label()
        label.set_label("Registrado em: {}".format(data['data'][8][:-7]))
        grid2.attach(label, 1, 3, 3, 1)

        button = Gtk.Button(width_request=100, height_request=40)
        button.set_label("Atualizar")
        button.connect("clicked", self.update_window, userId)
        grid2.attach(button, 4, 3, 1, 1)
        
        button = Gtk.Button(width_request=100)
        button.set_label("Fechar")
        button.connect("clicked", self.destroy_window)
        grid2.attach(button, 5, 3, 1, 1)
    
    def show_new_address(self, widget, clientId):
        win = UiNewAddress(clientId)
        win.show_all()
    
    def show_new_pin(self, widget, data):
        win = UiNewPin(data)
        win.show_all()
    
    def show_update_name(self, widget, userId, name):
        win = UiUpdateUserName(userId, name)
        win.show_all()
    
    def show_change_contacts(self, widget, data):
        win = UiChangeContacts(data)
        win.show_all()
    
    def show_new_level(self, widget, data):
        win = UiChangeLevel(data)
        win.show_all()
    
    def update_window(self, widget, userId):
        self.destroy()
        win = UiUserInfo(userId)
        win.show_all()
    
    def destroy_window(self, widget):
        return self.destroy()

class UiNewUser(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Cadastro de usuário", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=20, halign="start")
        label.set_markup("<span size='20000'>Cadastro de usuário</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nome
        label = Gtk.Label(halign="start")
        label.set_markup("Nome completo:<span color='red'>*</span>")
        self.name = Gtk.Entry(max_length=120)
        grid.attach(label, 1, 2, 2, 1)
        grid.attach(self.name, 1, 3, 2, 1)

        # Username
        label = Gtk.Label(halign="start")
        label.set_markup("Username:<span color='red'>*</span>")
        self.username = Gtk.Entry(max_length=120)
        self.username.set_input_purpose(Gtk.InputPurpose.NUMBER)
        grid.attach(label, 3, 2, 1, 1)
        grid.attach(self.username, 3, 3, 1, 1)

        # PIN
        label = Gtk.Label(halign="start")
        label.set_markup("PIN:<span color='red'>*</span> (4 números)")
        self.pin = Gtk.Entry(max_length=4)
        grid.attach(label, 3, 4, 1, 1)
        grid.attach(self.pin, 3, 5, 1, 1)

        # Nível de permisão
        label = Gtk.Label(halign="start")
        label.set_markup("Nível de permisão:<span color='red'>*</span>")
        grid.attach(label, 1, 4, 2, 1)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(box, 1, 5, 2, 1)

        self.level = 1
        radiobutton1 = Gtk.RadioButton(label="Nível 1")
        radiobutton1.connect("toggled", self.on_radio_button_toggled)
        box.pack_start(radiobutton1, True, True, 0)
        radiobutton2 = Gtk.RadioButton(label="Nível 2", group=radiobutton1)
        radiobutton2.connect("toggled", self.on_radio_button_toggled)
        box.pack_start(radiobutton2, True, True, 0)
        radiobutton3 = Gtk.RadioButton(label="Nível 3", group=radiobutton1)
        radiobutton3.connect("toggled", self.on_radio_button_toggled)
        box.pack_start(radiobutton3, True, True, 0)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 6, 3, 1)

        # E-mail
        label = Gtk.Label(halign="start")
        label.set_label("E-mail:")
        self.email = Gtk.Entry(max_length=200)
        self.email.set_input_purpose(Gtk.InputPurpose.EMAIL)
        grid.attach(label, 1, 7, 1, 1)
        grid.attach(self.email, 1, 8, 1, 1)

        # Telefone
        label = Gtk.Label(halign="start")
        label.set_markup("Telefone:<span color='red'>*</span>")
        self.phone = Gtk.Entry(max_length=20)
        self.phone.set_input_purpose(Gtk.InputPurpose.PHONE)
        grid.attach(label, 2, 7, 1, 1)
        grid.attach(self.phone, 2, 8, 1, 1)

        # Aniversário
        label = Gtk.Label(halign="start")
        label.set_markup("Aniversário:<span color='red'>*</span>")
        self.birthday = Gtk.Entry(max_length=10)
        grid.attach(label, 3, 7, 1, 1)
        grid.attach(self.birthday, 3, 8, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 9, 3, 1)

        # Enviar
        submit = Gtk.Button(label="Próximo", height_request=40)
        submit.connect("clicked", self.submit_user)
        grid.attach(submit, 1, 10, 3, 1)

    def on_radio_button_toggled(self, radiobutton):
        if radiobutton.get_active():
            self.level = radiobutton.get_label()[-1:]
    
    def submit_user(self, widget):
        username = self.username.get_text().strip()
        user = SbDUser()
        rData = user.new([self.name.get_text().strip(), username, self.pin.get_text().strip(), self.level, self.phone.get_text().strip(), self.email.get_text().strip(), self.birthday.get_text().strip()])
        if rData['rStatus']==11:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        elif rData['rStatus']==9:
            return UiDialog("Erro!", "Username já cadastrado.")
        elif rData['rStatus']==0:
            self.destroy()
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")
        else:
            self.destroy()
            data = user.get_id_by_username(username)
            if data['rStatus']==1:
                win = UiNewAddress(data['data'])
                win.show_all()

class UiNewAddress(Gtk.Window):

    def __init__(self, userId):
        Gtk.Window.__init__(self, title="Endereço", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Endereço</span>")
        grid.attach(label, 1, 1, 1, 1)

        # CEP
        label = Gtk.Label(halign="start")
        label.set_label("CEP:")
        self.cep = Gtk.Entry(max_length=10)
        self.cep.set_input_purpose(Gtk.InputPurpose.NUMBER)
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.cep, 1, 3, 1, 1)

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
        self.state.set_text("Espírito Santo")
        grid.attach(label, 1, 10, 1, 1)
        grid.attach(self.state, 1, 11, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=20, margin_bottom=20)
        grid.attach(separator, 1, 12, 3, 1)

        # Enviar
        submit = Gtk.Button(label="Enviar", height_request=40)
        submit.connect("clicked", self.submit_address, userId)
        grid.attach(submit, 1, 13, 2, 1)

        # Cancelar
        button = Gtk.Button(label="Fechar", height_request=40)
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 3, 13, 1, 1)
    
    def destroy_window(self, widget):
        return self.destroy()
    
    def submit_address(self, widget, userId):
        house = self.house.get_text().strip()
        if len(house)==0:
            house = "SN"
        if len(self.street.get_text().strip())==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if len(self.bairro.get_text().strip())==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if len(self.city.get_text().strip())==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        insert = SbDUser(userId)
        result = insert.insert_address([self.cep.get_text().strip(), house, self.street.get_text().strip(), self.complement.get_text().strip(), self.bairro.get_text().strip(), self.city.get_text().strip(), self.state.get_text().strip(), 'Brasil'])
        self.destroy()
        if not result:
            return UiDialog("Erro ao enviar", "Erro ao inserir as informações no banco de dados.")

class UiChangeLevel(Gtk.Window):

    def __init__(self, data):
        Gtk.Window.__init__(self, title="Alterar nível de permissão", window_position="center")
        self.set_resizable(False)

        check = SbSession()
        if check.check_level(True)!=3:
            UiDialog('Erro de permissão!', 'Somente usuários com o nível 3 podem alterar permissões.')
            return self.destroy()
        
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Alterar nível de permissão</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nível de permisão
        label = Gtk.Label(halign="start")
        label.set_markup("Nível de permisão:<span color='red'>*</span>")
        grid.attach(label, 1, 2, 1, 1)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(box, 1, 3, 1, 1)

        self.level = data[1]
        radiobutton1 = Gtk.RadioButton(label="Nível 1")
        radiobutton1.connect("toggled", self.on_radio_button_toggled)
        box.pack_start(radiobutton1, True, True, 0)
        radiobutton2 = Gtk.RadioButton(label="Nível 2", group=radiobutton1)
        radiobutton2.connect("toggled", self.on_radio_button_toggled)
        box.pack_start(radiobutton2, True, True, 0)
        radiobutton3 = Gtk.RadioButton(label="Nível 3", group=radiobutton1)
        radiobutton3.connect("toggled", self.on_radio_button_toggled)
        box.pack_start(radiobutton3, True, True, 0)

        if self.level==1:
            radiobutton1.set_active(True)            
        elif self.level==2:
            radiobutton2.set_active(True)            
        else:
            radiobutton3.set_active(True)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 4, 1, 1)

        button = Gtk.Button(height_request=40)
        button.set_label("Atualizar")
        button.connect("clicked", self.submit, data[0])
        grid.attach(button, 1, 5, 1, 1)
    
    def on_radio_button_toggled(self, radiobutton):
        if radiobutton.get_active():
            self.level = radiobutton.get_label()[-1:]
    
    def submit(self, widget, userId):
        change = SbDUser(userId)
        self.destroy()
        if not change.change_level(self.level):
            return UiDialog("Erro!", "Erro ao enviar dados.")

class UiNewPin(Gtk.Window):

    def __init__(self, data):
        Gtk.Window.__init__(self, title="Alterar PIN", window_position="center")
        self.set_resizable(False)
        
        session = SbSession()
        info = session.get_info()
        if info['user']['username']!=data[1]:
            if info['user']['level']!=3:
                UiDialog('Erro de permissão!', 'Somente usuários com o nível 3 podem alterar senhas de outros usuários.')
                return self.destroy()
        
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Alterar PIN</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nova senha
        label = Gtk.Label(halign="start")
        label.set_label("Novo PIN: (4 números)")
        self.pin = Gtk.Entry(max_length=4)
        self.pin.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.pin.connect("activate", self.update_pin, data[0])
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.pin, 1, 3, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 8, 1, 1)

        # Enviar
        button = Gtk.Button(label="Atualizar", height_request=40)
        button.connect("clicked", self.update_pin, data[0])
        grid.attach(button, 1, 9, 1, 1)
    
    def update_pin(self, widget, userId):
        pin = self.pin.get_text().strip()
        if not pin or len(str(pin))<4 or len(str(pin))>4:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if not pin.isdigit():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        submit = SbDUser(userId)
        self.destroy()
        if not submit.change_pin(pin):
            return UiDialog("Erro!", "Erro ao enviar dados.")

class UiUpdateUserName(Gtk.Window):

    def __init__(self, userId, name):
        Gtk.Window.__init__(self, title="Alterar nome", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30)
        label.set_markup("<span size='20000'>Alterar nome do usuário</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nome
        label = Gtk.Label(label="Nome completo:")
        self.name = Gtk.Entry(width_request=350)
        self.name.set_text(name)
        self.name.connect("activate", self.update_name, userId)
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.name, 1, 3, 1, 1)

        # Enviar
        button = Gtk.Button(label="Atualizar", height_request=40)
        button.connect("clicked", self.update_name, userId)
        grid.attach(button, 1, 4, 1, 1)
    
    def update_name(self, widget, userId):
        name = self.name.get_text().strip()
        if not name:
            return UiDialog("Entrada inválida!", "Por favor preencha os campos corretamente.")
        submit = SbDUser(userId)
        self.destroy()
        if not submit.change_name(name):
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")

class UiChangeContacts(Gtk.Window):

    def __init__(self, data):
        Gtk.Window.__init__(self, title="Alterar informações de contato", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30)
        label.set_markup("<span size='20000'>Alterar informações de contato</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Telefone
        label = Gtk.Label(label="Número:")
        self.number = Gtk.Entry(max_length=20, width_request=200)
        self.number.set_text(data[1])
        self.number.connect("activate", self.update, data[0])
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.number, 1, 3, 1, 1)

        # E-mail
        label = Gtk.Label(label="E-mail:")
        self.email = Gtk.Entry(max_length=200, width_request=200)
        self.email.set_text(data[2])
        self.email.connect("activate", self.update, data[0])
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.email, 1, 5, 1, 1)

        # Enviar
        button = Gtk.Button(label="Atualizar", height_request=40)
        button.connect("clicked", self.update, data[0])
        grid.attach(button, 1, 6, 1, 1)

    def update(self, widget, userId):
        submit = SbDUser(userId)
        if not submit.change_contacts([self.number.get_text(), self.email.get_text()]):
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        return self.destroy()