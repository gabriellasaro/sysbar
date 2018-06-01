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
from sysbar.ui.products.new import UiNewProduct
from sysbar.ui.products.products import UiListProducts
from sysbar.ui.client import UiCustomerList
from sysbar.ui.user import UiUserList
from sysbar.ui.about import AboutSystem
from sysbar.ui.dialog import UiDialog
from sysbar.lib.settings import SbStoreInfo, SbTheme, SbBackup
from sysbar.lib.session import SbSession
class UiAdmin(Gtk.Window):
        
    def __init__(self):
        Gtk.Window.__init__(self, title="Administração - SysBar", window_position="center")
        self.set_resizable(False)
        wGrid = Gtk.Grid()
        self.add(wGrid)

        # Título
        label = Gtk.Label(margin=20, halign="start")
        label.set_markup("<span size='20000'>Administração</span>")
        wGrid.attach(label, 1, 1, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow(width_request=340, height_request=400)
        wGrid.attach(scrolledwindow, 1, 2, 1, 1)

        viewport = Gtk.Viewport()
        scrolledwindow.add(viewport)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=20)
        viewport.add(box)

        button = Gtk.Button(height_request=70)
        button.set_label("Novo produto")
        button.connect("clicked", self.show_new_product)
        box.pack_start(button, True, True, 5)

        button = Gtk.Button(height_request=70)
        button.set_label("Produtos")
        button.connect("clicked", self.show_list_product)
        box.pack_start(button, True, True, 5)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator, True, True, 10)
        
        button = Gtk.Button(height_request=70)
        button.set_label("Clientes")
        button.connect("clicked", self.show_customer_list)
        box.pack_start(button, True, True, 5)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator, True, True, 10)

        button = Gtk.Button(height_request=70)
        button.set_label("Usuários")
        button.connect("clicked", self.show_users)
        box.pack_start(button, True, True, 5)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator, True, True, 10)

        button = Gtk.Button(height_request=70)
        button.set_label("Estabelecimento")
        button.connect("clicked", self.show_store_info)
        box.pack_start(button, True, True, 5)

        button = Gtk.Button(height_request=70)
        button.set_label("Backup")
        button.connect("clicked", self.show_backup)
        box.pack_start(button, True, True, 5)

        button = Gtk.Button(height_request=70)
        button.set_label("Licenciado")
        button.connect("clicked", self.show_license)
        box.pack_start(button, True, True, 5)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(separator, True, True, 10)

        button = Gtk.Button(height_request=70)
        button.set_label("Suporte")
        button.connect("clicked", self.show_support)
        box.pack_start(button, True, True, 5)

        button = Gtk.Button(height_request=70)
        button.set_label("Temas")
        button.connect("clicked", self.show_theme)
        box.pack_start(button, True, True, 5)

        button = Gtk.Button(height_request=70)
        button.set_label("Sobre SysBar")
        wAbout = AboutSystem()
        button.connect("clicked", wAbout.about_dialog)
        box.pack_start(button, True, True, 5)
        
    def show_list_product(self, widget):
        win = UiListProducts()
        win.show_all()
    
    def show_new_product(self, widget):
        win = UiNewProduct()
        win.show_all()
    
    def show_customer_list(self, widget):
        win = UiCustomerList()
        win.show_all()
    
    def show_store_info(self, widget):
        win = UiStoreInfo()
        win.show_all()
    
    def show_support(self, widget):
        win = UiSupport()
        win.show_all()
    
    def show_theme(self, widget):
        win = UiTheme()
        win.show_all()
    
    def show_license(self, widget):
        win = UiLicense()
        win.show_all()
    
    def show_backup(self, widget):
        win = UiBackup()
        win.show_all()
    
    def show_users(self, widget):
        win = UiUserList()
        win.show_all()
    
class UiStoreInfo(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Informações do estabelecimento", window_position="center")
        self.set_resizable(False)
        
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)
        
        # Título
        label = Gtk.Label(margin_bottom=20, halign="start")
        label.set_markup("<span size='20000'>Informações do Estabelecimento</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Nome da empresa
        label = Gtk.Label(halign="start")
        label.set_label("Nome da empresa:")
        self.name = Gtk.Entry(width_request=300)
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.name, 1, 3, 1, 1)

        # CNPJ
        label = Gtk.Label(halign="start")
        label.set_label("CNPJ:")
        self.cnpj = Gtk.Entry()
        grid.attach(label, 2, 2, 1, 1)
        grid.attach(self.cnpj, 2, 3, 1, 1)

        # Telefone
        label = Gtk.Label(halign="start")
        label.set_label("Telefone:")
        self.phone = Gtk.Entry()
        grid.attach(label, 3, 2, 1, 1)
        grid.attach(self.phone, 3, 3, 1, 1)

        # Logradouro
        label = Gtk.Label(halign="start")
        label.set_label("Logradouro:")
        self.street = Gtk.Entry()
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.street, 1, 5, 1, 1)

        # Número do local
        label = Gtk.Label(halign="start")
        label.set_label("Número do local:")
        self.number = Gtk.Entry()
        grid.attach(label, 2, 4, 1, 1)
        grid.attach(self.number, 2, 5, 1, 1)

        # CEP
        label = Gtk.Label(halign="start")
        label.set_label("CEP:")
        self.cep = Gtk.Entry()
        grid.attach(label, 3, 4, 1, 1)
        grid.attach(self.cep, 3, 5, 1, 1)

        # Bairro/Distrito
        label = Gtk.Label(halign="start")
        label.set_label("Bairro:")
        self.district = Gtk.Entry()
        grid.attach(label, 1, 6, 1, 1)
        grid.attach(self.district, 1, 7, 1, 1)

        # Cidade
        label = Gtk.Label(halign="start")
        label.set_label("Cidade:")
        self.city = Gtk.Entry()
        grid.attach(label, 2, 6, 1, 1)
        grid.attach(self.city, 2, 7, 1, 1)

        # País/Nação
        label = Gtk.Label(halign="start")
        label.set_label("País/Nação:")
        self.nation = Gtk.Entry()
        # self.nation.set_editable(False)
        grid.attach(label, 3, 6, 1, 1)
        grid.attach(self.nation, 3, 7, 1, 1)

        # Estado/Região
        label = Gtk.Label(halign="start")
        label.set_label("Estado/Região:")
        self.state = Gtk.Entry()
        grid.attach(label, 1, 8, 1, 1)
        grid.attach(self.state, 1, 9, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 10, 3, 1)

        # Data config
        config = SbStoreInfo()
        data = config.get_store_info()
        if data['rStatus']==1:
            self.set_data(data['data'])
                
        # Enviar
        userLevel = SbSession()
        if userLevel.check_level()==3:
            button = Gtk.Button(height_request=40)
            button.set_label("Enviar/Atualizar")
            button.connect("clicked", self.submit_update)
            grid.attach(button, 1, 11, 3, 1)
        else:
            label = Gtk.Label(halign="center", margin_top=10, margin_bottom=10)
            label.set_label("Este usuário não possui permissão para atualizar essas informações.")
            grid.attach(label, 1, 11, 3, 1)
    
    def set_data(self, data):
        self.name.set_text(data['store']['name'])
        self.cnpj.set_text(data['store']['cnpj'])
        self.phone.set_text(data['store']['phone'])
        self.street.set_text(data['store']['logradouro'])
        self.number.set_text(data['store']['number'])
        self.cep.set_text(data['store']['cep'])
        self.state.set_text(data['store']['state'])
        self.district.set_text(data['store']['district'])
        self.city.set_text(data['store']['city'])
        self.nation.set_text(data['store']['nation'])
    
    def submit_update(self, widget):
        data = [
            self.name.get_text().strip(),
            self.cnpj.get_text().strip(),
            self.street.get_text().strip(),
            self.number.get_text().strip(),
            self.cep.get_text().strip(),
            self.district.get_text().strip(),
            self.city.get_text().strip(),
            self.state.get_text().strip(),
            self.nation.get_text().strip(),
            self.phone.get_text().strip()
        ]
        submit = SbStoreInfo()
        if not submit.set_store_info(data):
            return UiDialog("Erro!", "Erro ao enviar dados.")
        else:
            return self.destroy()

class UiSupport(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Suporte", window_position="center")
        self.set_resizable(False)

        grid = Gtk.Grid(margin=40)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=20, halign="center")
        label.set_markup("<span size='21000'>Suporte</span>")
        grid.attach(label, 1, 1, 1, 1)

        label = Gtk.Label()
        label.set_label("Contado:")
        grid.attach(label, 1, 2, 1, 1)

        label = Gtk.Label()
        label.set_label("Se precissar de ajuda não deixe de entrar em contato, estamos a disposição!")
        grid.attach(label, 1, 3, 1, 1)

        label = Gtk.LinkButton("https://www.sysbar.info/#cont", "Acessar www.sysbar.info")
        grid.attach(label, 1, 4, 1, 1)

        label = Gtk.LinkButton("http://api.whatsapp.com/send?phone=552737434062", "Whatsapp: (27) 37434062")
        grid.attach(label, 1, 5, 1, 1)

class UiTheme(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Temas", window_position="center")
        self.set_resizable(False)

        grid = Gtk.Grid(margin=40)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start", margin_right=20)
        label.set_markup("<span size='20000'>Temas</span>")
        grid.attach(label, 1, 1, 1, 1)

        self.theme = Gtk.RadioButton(label="Tema Nativo", halign="start", margin_right=100, margin_bottom=10)
        self.theme.connect("toggled", self.change_theme)
        self.theme2 = Gtk.RadioButton(label="Tema SysBar Lite", group=self.theme, halign="start")
        self.theme2.connect("toggled", self.change_theme)

        status = SbTheme()
        if status.get_theme():
            self.theme2.set_active(True)
        else:
            self.theme.set_active(True)
                
        grid.attach(self.theme, 1, 2, 1, 1)
        grid.attach(self.theme2, 1, 3, 1, 1)
    
    def change_theme(self, widget):
        submit = SbTheme()
        if self.theme2.get_active():
            submit.change(True)
        else:
            submit.change(False)

class UiLicense(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Licenciado", window_position="center")
        self.set_resizable(False)

        grid = Gtk.Grid(margin=40)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start", margin_right=20)
        label.set_markup("<span size='20000'>Licenciado</span>")
        grid.attach(label, 1, 1, 1, 1)

        label = Gtk.Label(margin_bottom=60, halign="center")
        info = SbStoreInfo()
        data = info.get_store_info()
        if data['rStatus']==1:
            label.set_label("Este software foi licenciado por SysBar para {}.".format(info.get_store_info()['data']['store']['name']))
        else:
            label.set_label("Este software foi licenciado.")
        
        grid.attach(label, 1, 2, 1, 1)

        label = Gtk.Label(halign="center")
        label.set_label("© COPYRIGHT 2018 SysBar")
        grid.attach(label, 1, 3, 1, 1)

        # progressBar = Gtk.ProgressBar(orientation=Gtk.Orientation.HORIZONTAL)

        # tempoTotal = 365
        # tempoAtual = 0
        # retorno = (tempoAtual*100)/tempoTotal
        # progressBar.set_fraction(retorno/100)
        # progressBar.set_text("{}/{}".format(tempoAtual, tempoTotal))
        # progressBar.set_show_text(True)
        # grid.attach(progressBar, 1, 2, 1, 1)

class UiBackup(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Backup", window_position="center")
        self.set_resizable(False)

        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        userLevel = SbSession()
        if userLevel.check_level()!=3:
            label = Gtk.Label(halign="center")
            label.set_label("Este usuário não possui permissão para essa função.")
            grid.attach(label, 1, 1, 1, 1)
        else:
            # Título
            label = Gtk.Label(margin_bottom=30, halign="center")
            label.set_markup("<span size='20000'>Fazer backup da base de dados?</span>")
            grid.attach(label, 1, 1, 2, 1)

            button = Gtk.Button(label="Não", height_request=40)
            button.connect("clicked", self.destroy_window)
            grid.attach(button, 1, 2, 1, 1)

            button = Gtk.Button(label="Sim", height_request=40)
            button.connect("clicked", self.create)
            grid.attach(button, 2, 2, 1, 1)
    
    def create(self, widget):
        data = SbBackup()
        data.create()
        return self.destroy()
    
    def destroy_window(self, widget):
        return self.destroy()