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
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from sysbar.lib.products import SbProducts, SbProductInsert, SbProductUpdate, SbCategories
from sysbar.lib.session import SbSession
from sysbar.ui.dialog import UiDialog
class UiListProducts(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Lista de produtos - SysBar", window_position="center")
        self.set_default_size(1000, 600)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Produtos:</span>")
        grid.attach(label, 1, 1, 1, 1)

        data = SbProducts()
        rData = data.get_product_list()
        # Lista
        self.liststore = Gtk.ListStore(int, str, str, str, int, str)
        # ID - BARCODE - NAME - PRICE - DISCOUNT - STOCK
        if rData['rStatus']==1:
            for item in rData['data']:
                price = "R$ {}".format(str(item[3]).replace(".", ","))
                if item[6]==0:
                    self.liststore.append([item[0], str(item[1]), item[2], price, item[4], "Desativado"])
                else:
                    self.liststore.append([item[0], str(item[1]), item[2], price, item[4], str(item[5])])
        
        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        treeview.set_search_column(2)
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.connect("row-activated", self.on_row_activated)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(treeview)
        grid.attach(scrolledwindow, 1, 2, 3, 1)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("ID")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Cód. barra")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Nome do Produto")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 2)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Preço de Venda")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 3)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Desc. Aniversario (%)")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 4)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Estoque")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 5)
        treeview.append_column(treeviewcolumn)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(separator, 4, 2, 1, 1)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Categorias:</span>")
        grid.attach(label, 5, 1, 1, 1)

        self.liststore2 = Gtk.ListStore(int, str)
        # ID - CATEGORY
        data = SbCategories()
        rCategories = data.get_categories()
        if rCategories['rStatus']==1:
            for item in rCategories['data']:
                self.liststore2.append([item[0], item[1]])
        
        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore2)
        treeview.set_search_column(1)
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        treeview.connect("row-activated", self.category_activated)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(treeview)
        grid.attach(scrolledwindow, 5, 2, 1, 1)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("Categoria")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
        treeview.append_column(treeviewcolumn)

        button = Gtk.Button(label="Novo produto", height_request=40, halign="start")
        button.connect("clicked", self.show_ui_new_product)
        grid.attach(button, 1, 3, 1, 1)

        button = Gtk.Button(label="Nova categoria", height_request=40, halign="start")
        button.connect("clicked", self.show_ui_new_category)
        grid.attach(button, 5, 3, 1, 1)

        button = Gtk.Button(label="Atualizar", height_request=40, halign="end")
        button.connect("clicked", self.update_window)
        grid.attach(button, 3, 3, 1, 1)
    
    def on_row_activated(self, widget, treepath, text):
        win = UiInfoProduct(self.liststore[treepath][0])
        win.show_all()

    def category_activated(self, widget, treepath, text):
        win = UiNewCategory(True, self.liststore2[treepath][0], self.liststore2[treepath][1])
        win.show_all()
        
    def show_ui_new_product(self, widget):
        win = UiNewProduct()
        win.show_all()
    
    def show_ui_new_category(self, widget):
        win = UiNewCategory()
        win.show_all()
    
    def update_window(self, widget):
        self.destroy()
        win = UiListProducts()
        win.show_all()
    
class UiNewCategory(Gtk.Window):

    def __init__(self, update=False, categoryId=None, name=None):
        Gtk.Window.__init__(self, window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        if update:
            userLevel = SbSession()
            if userLevel.check_level()<2:
                UiDialog("Erro de permissão", "Este usuário não possui permissão para acessar as informações.")
                return self.destroy()
            label = Gtk.Label(margin_bottom=30)
            label.set_markup("<span size='20000'>Atualizar categoria</span>")
            self.set_title("Atualizar categoria")
        else:
            label = Gtk.Label(margin_bottom=30)
            label.set_markup("<span size='20000'>Adicionar nova categoria</span>")
            self.set_title("Adicionar nova categoria")
        grid.attach(label, 1, 1, 2, 1)

        # Nome
        label = Gtk.Label(label="Nome da categoria:")
        self.name = Gtk.Entry(width_request=350)
        grid.attach(label, 1, 2, 2, 1)
        grid.attach(self.name, 1, 3, 2, 1)

        # Enviar
        button = Gtk.Button(height_request=40)
        if update:
            button.set_label("Atualizar")
            button.connect("clicked", self.update_category, categoryId)
            self.name.connect("activate", self.update_category, categoryId)
            self.name.set_text(name)
        else:
            button.set_label("Enviar")
            self.name.connect("activate", self.submit_category)
            button.connect("clicked", self.submit_category)
        grid.attach(button, 1, 4, 1, 1)

        # Cancelar
        button = Gtk.Button(label="Fechar")
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 2, 4, 1, 1)

    def destroy_window(self, widget):
        return self.destroy()
    
    def update_category(self, widget, categoryId):
        name = self.name.get_text()
        if len(name)==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        self.destroy()
        submit = SbCategories(categoryId)
        if not submit.update_category(name):
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")
    
    def submit_category(self, widget):
        name = self.name.get_text()
        if len(name)==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        self.destroy()
        submit = SbCategories()
        if not submit.insert_category(name):
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")

class UiInfoProduct(Gtk.Window):
    
    def __init__(self, idProduct):
        Gtk.Window.__init__(self, title="Informações do produto - SysBar", window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        product = SbProducts(idProduct)
        self.dataProduct = product.get_product_information()
        self.idProduct = idProduct
        if self.dataProduct['rStatus']==0:
            # Título
            label = Gtk.Label(margin_bottom=30, halign="start")
            label.set_markup("<span size='20000'>Informações do produto</span>")
            grid.attach(label, 1, 1, 1, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("<span color='red'>Não encontramos o produto!</span>")
            grid.attach(label, 1, 2, 1, 1)
        else:
            # Título
            label = Gtk.Label(margin_bottom=30, halign="start")
            label.set_markup("<span size='20000'>Informações do produto</span>")
            grid.attach(label, 1, 1, 1, 1)

            imgName = "static/{}".format(self.dataProduct['data'][3])
            pix = Pixbuf.new_from_file_at_size(imgName, 120, 100)
            img = Gtk.Image(margin_left=20, halign="start")
            img.set_from_pixbuf(pix)
            grid.attach(img, 1, 2, 1, 4)

            separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
            grid.attach(separator, 2, 2, 1, 9)
            
            label = Gtk.Label(halign="start")
            label.set_markup("ID do produto: <span color='blue'>{}</span>".format(self.dataProduct['data'][0]))
            grid.attach(label, 3, 2, 1, 1)

            label = Gtk.Label(halign="start")
            if len(str(self.dataProduct['data'][1]))==0:
                label.set_markup("Código de Barras: <span color='red'>Não informado.</span>")
            else:
                label.set_markup("Código de Barras: <span color='blue'>{}</span>".format(self.dataProduct['data'][1]))
            grid.attach(label, 3, 3, 1, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("Nome: <span color='blue'>{}</span>".format(self.dataProduct['data'][2]))
            grid.attach(label, 1, 7, 1, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("Preço de Venda: <span color='blue'>R$ {}</span>".format(str(self.dataProduct['data'][5]).replace(".", ",")))
            grid.attach(label, 1, 8, 1, 1)

            label = Gtk.Label(halign="start")
            userLevel = Session()
            if userLevel.check_level_user()>=2:
                label.set_markup("Preço de custo: <span color='blue'>R$ {}</span>".format(str(self.dataProduct['data'][6]).replace(".", ",")))
            else:
                label.set_markup("Preço de custo: <span color='red'>Ind. sem permissão</span>")
            grid.attach(label, 1, 9, 1, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("Desconto para aniversariante: <span color='blue'>{}%</span>".format(self.dataProduct['data'][7]))
            grid.attach(label, 1, 10, 1, 1)

            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            grid.attach(separator, 3, 4, 1, 1)
            
            label = Gtk.Label(halign="start")
            label.set_markup("Categoria: <span color='blue'>{}</span>".format(self.dataProduct['data'][22]))
            grid.attach(label, 3, 5, 1, 1)

            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            grid.attach(separator, 3, 6, 1, 1)

            label = Gtk.Label(halign="start")
            if self.dataProduct['data'][17] in ['P', 'M', 'G']:
                if self.dataProduct['data'][17]=='P':
                    label.set_markup("Tamanho: <span color='blue'>Pequeno ({})</span>".format(self.dataProduct['data'][17]))
                elif  self.dataProduct['data'][17]=='M':
                    label.set_markup("Tamanho: <span color='blue'>Médio ({})</span>".format(self.dataProduct['data'][17]))
                else:
                    label.set_markup("Tamanho: <span color='blue'>Grande ({})</span>".format(self.dataProduct['data'][17]))
            elif self.dataProduct['data'][17] in ['Kg', 'g']:
                label.set_markup("Peso: <span color='blue'>{} {}</span>".format(self.dataProduct['data'][18], self.dataProduct['data'][17]))
            else:
                label.set_markup("Volume: <span color='blue'>{} {}</span>".format(self.dataProduct['data'][18], self.dataProduct['data'][17]))
            grid.attach(label, 3, 7, 1, 1)

            label = Gtk.Label(halign="start")
            label.set_markup("Pessoas servidas: <span color='blue'>{}</span>".format(self.dataProduct['data'][19]))
            grid.attach(label, 3, 8, 1, 1)

            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            grid.attach(separator, 3, 9, 1, 1)

            if self.dataProduct['data'][9]==1:
                label = Gtk.Label(halign="start")
                label.set_markup("Estoque: <span color='blue'>{} unidades</span>".format(self.dataProduct['data'][8]))
                grid.attach(label, 3, 10, 1, 1)

            button = Gtk.Button(margin_top=25, height_request=40)
            button.set_label("Editar")
            button.connect("clicked", self.show_ui_update_product)
            grid.attach(button, 1, 11, 1, 1)

            button = Gtk.Button(margin_top=25, height_request=40)
            button.set_label("Fechar")
            button.connect("clicked", self.destroy_window)
            grid.attach(button, 3, 11, 1, 1)
    
    def show_ui_update_product(self, widget):
        self.destroy()
        win = UiNewProduct(True, self.dataProduct)
        win.show_all()
    
    def destroy_window(self, widget):
        self.destroy()

class UiNewProduct(Gtk.Window):

    def __init__(self, update=False, data=None):
        Gtk.Window.__init__(self, window_position="center")
        self.set_resizable(False)
        userLevel = SbSession()
        if userLevel.check_level()<2:
            UiDialog("Erro de permissão", "Este usuário não possui permissão para acessar as informações.")
            return self.destroy()

        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        title = Gtk.Label(margin_bottom=30)
        if not update:
            self.set_title("Novo produto - SysBar")
            title.set_markup("<span size='21000'>Novo produto:</span>")
        else:
            self.set_title("Atualizar produto - SysBar")            
            title.set_markup("<span size='21000'>Atualizar produto:</span>")
        grid.attach(title, 1, 1, 1, 1)

        # Tipo
        liststore = Gtk.ListStore(str)
        for item in ["Escolher", "Líquido", "Peso", "Tamanho"]:
            liststore.append([item])

        self.typeUnity = Gtk.ComboBox(width_request=150)
        self.typeUnity.set_model(liststore)
        self.typeUnity.set_active(0)
        self.typeUnity.connect("changed", self.on_event_01)

        cellrenderertext = Gtk.CellRendererText()
        self.typeUnity.pack_start(cellrenderertext, True)
        self.typeUnity.add_attribute(cellrenderertext, "text", 0)

        label = Gtk.Label(halign="start")
        label.set_text("Tipo de produto:")
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.typeUnity, 1, 3, 1, 1)

        # Unidade
        self.unity = Gtk.ComboBoxText()
        listItems = [("0", "Escolher"), ("L", "Litros (L)"), ("Ml", "Mililitros (Ml)"),
         ("Kg", "Quilogramas (Kg)"), ("g", "Gramas (g)"),
          ("P", "Pequeno (P)"), ("M", "Médio (M)"), ("G", "Grande (G)")]
        for item in listItems:
            self.unity.append(item[0], item[1])
        self.unity.set_active_id("0")

        label = Gtk.Label(halign="start")
        label.set_label("Unidade:")
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.unity, 1, 5, 1, 1)

        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 1, 6, 1, 1)

        # Quantidade
        label = Gtk.Label(halign="start")
        label.set_label("Peso/Volume:")
        self.qUnity = Gtk.Entry(max_length=4)
        grid.attach(label, 1, 7, 1, 1)
        grid.attach(self.qUnity, 1, 8, 1, 1)

        # Pessoas servidas
        label = Gtk.Label(halign="start")
        label.set_label("Pessoas servidas:")
        self.people = Gtk.Entry(max_length=4)
        grid.attach(label, 1, 9, 1, 1)
        grid.attach(self.people, 1, 10, 1, 1)

        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL, margin_left=15, margin_right=15)
        grid.attach(separator, 2, 2, 1, 9)

        # Label info
        label = Gtk.Label(halign="start")
        label.set_label("Configurações:")
        grid.attach(label, 3, 2, 1, 1)

        # Cardápio virtual
        self.cvirtual = Gtk.CheckButton()
        self.cvirtual.set_label("Cardápio Virtual")
        self.cvirtual.set_active(True)
        grid.attach(self.cvirtual, 3, 3, 1, 1)

        # Delivery
        self.delivery = Gtk.CheckButton()
        self.delivery.set_label("Disponível para Delivery")
        self.delivery.set_active(False)
        grid.attach(self.delivery, 3, 4, 1, 1)

        # Pedido especial
        self.special = Gtk.CheckButton()
        self.special.set_label("Pedido Especial")
        self.special.set_active(False)
        grid.attach(self.special, 3, 5, 1, 1)

        label = Gtk.Label(halign="start")
        label.set_label("Pedido Especial:\rautoriza ao cliente, solicitar\ra remoção de ingredientes")
        grid.attach(label, 3, 6, 1, 2)
        
        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 3, 8, 1, 1)

        # Categoria
        dataCategories = SbCategories()
        rData = dataCategories.get_categories()
        
        self.category = Gtk.ComboBoxText(width_request=200)
        self.category.append("0", "Escolher")
        if rData['rStatus']==1:
            for item in rData['data']:
                self.category.append(str(item[0]), item[1])

        self.category.set_active_id("0")
        label = Gtk.Label(halign="start")
        label.set_label("Categoria:")
        grid.attach(label, 3, 9, 1, 1)
        grid.attach(self.category, 3, 10, 1, 1)

        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=20, margin_bottom=20)
        grid.attach(separator, 1, 11, 3, 1)

        # Enviar
        button = Gtk.Button(height_request=40)
        if not update:
            button.set_label("Próximo")
            button.connect("clicked", self.create_product)
        else:
            button.set_label("Atualizar")
            button.connect("clicked", self.update_product, data)
        grid.attach(button, 1, 12, 3, 1)

        if update:
            button = Gtk.Button(label="Pular etapa", height_request=40)
            button.connect("clicked", self.skip_step_1, data)
            grid.attach(button, 1, 13, 3, 1)
            self.set_ui_update_product(data)
        
    def on_event_01(self, widget):
        if widget.get_active() == 1:
            self.unity.remove_all()
            for item in [("0", "Escolher"), ("L", "Litros (L)"), ("Ml", "Mililitros (Ml)")]:
                self.unity.append(item[0], item[1])
            self.unity.set_active_id("L")
            self.qUnity.set_editable(True)            
        elif widget.get_active() == 2:
            self.unity.remove_all()            
            for item in [("0", "Escolher"), ("Kg", "Quilogramas (Kg)"), ("g", "Gramas (g)")]:
                self.unity.append(item[0], item[1])
            self.unity.set_active_id("Kg")
            self.qUnity.set_editable(True)            
        elif widget.get_active() == 3:
            self.unity.remove_all()            
            for item in [("0", "Escolher"), ("P", "Pequeno (P)"), ("M", "Médio (M)"), ("G", "Grande (G)")]:
                self.unity.append(item[0], item[1])
            self.unity.set_active_id("M")
            self.qUnity.set_text("0")
            self.qUnity.set_editable(False)
        else:
            self.unity.set_active(0)
    
    def set_ui_update_product(self, data):
        self.idProduct = data['data'][0]
        self.unity.set_active_id(data['data'][17])
        self.qUnity.set_text(str(data['data'][18]))
        self.people.set_text(str(data['data'][19]))
        self.category.set_active_id(str(data['data'][13]))
        self.cvirtual.set_active(bool(data['data'][14]))
        self.special.set_active(bool(data['data'][15]))
        self.delivery.set_active(bool(data['data'][16]))

    def simple_remove_letters(self, text):
        text = text.replace(",", "")
        text = text.replace(".", "")
        return text
    
    def skip_step_1(self, widget, data):
        self.destroy()
        win = UiNPStep2(True, data)
        win.show_all()
    
    def update_product(self, widget, data):
        unity = self.unity.get_active_id()
        if unity == "0":
            return UiDialog("Preencha os campos", "Por favor preencha todos os campos.")            
        amount = self.qUnity.get_text()
        amount = amount.replace(",", ".")
        if not self.simple_remove_letters(amount).isnumeric() or len(amount)==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        category = self.category.get_active_id()
        if category == "0":
            return UiDialog("Preencha os campos", "Por favor preencha todos os campos.")
        people = self.people.get_text()
        if len(people)==0:
            people = "0"
        elif not people.isdigit():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        elif int(people)<0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        cvirtual = self.cvirtual.get_active()
        delivery = self.delivery.get_active()
        special = self.special.get_active()
        self.destroy()
        submit = SbProductUpdate()
        submit.set_product_id(self.idProduct)
        if not submit.update_meta_product(cvirtual, special, delivery, unity, amount, people, category):
            return UiDialog("Erro ao enviar dados", "Erro ao enviar dados. Por favor, tente novamente.")
        win = UiNPStep2(True, data)
        win.show_all()
    
    def create_product(self, widget):
        unity = self.unity.get_active_id()
        if unity == "0":
            return UiDialog("Preencha os campos", "Por favor preencha todos os campos.")            
        amount = self.qUnity.get_text()
        amount = amount.replace(",", ".")
        if not self.simple_remove_letters(amount).isnumeric() or len(amount)==0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")                
        category = self.category.get_active_id()
        if category == "0":
            return UiDialog("Preencha os campos", "Por favor preencha todos os campos.")
        people = self.people.get_text()
        if len(people)==0:
            people = "0"
        elif not people.isdigit():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        elif int(people)<0:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        cvirtual = self.cvirtual.get_active()
        delivery = self.delivery.get_active()
        special = self.special.get_active()
        submit = SbProductInsert()
        self.destroy()
        if not submit.insert_meta_product(cvirtual, special, delivery, unity, amount, people, category):
            return UiDialog("Erro ao enviar dados", "Erro ao enviar dados. Por favor, tente novamente.")
        # Obter ID
        win = UiNPStep2(False, submit.get_product_id())
        win.show_all()

class UiNPStep2(Gtk.Window):

    def __init__(self, update=False, data=None):
        Gtk.Window.__init__(self, window_position="center")
        self.set_resizable(False)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        title = Gtk.Label(margin_bottom=30, halign="start")
        if not update:
            self.idProduct = data
            self.set_title("Novo produto - SysBar")
            title.set_markup("<span size='21000'>Novo produto:</span>")
        else:
            self.idProduct = data['data'][0]
            self.set_title("Atualizar produto - SysBar")
            title.set_markup("<span size='21000'>Atualizar produto:</span>")
        grid.attach(title, 1, 1, 1, 1)

        # Código de barras
        label = Gtk.Label(halign="start")
        label.set_label("Código de barra: (Se houver)")
        self.barcode = Gtk.Entry(max_length=120, halign="start")
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.barcode, 1, 3, 1, 1)

        # Nome do produto
        label = Gtk.Label(halign="start")
        label.set_label("Nome do produto:*")
        self.name = Gtk.Entry(max_length=120)
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.name, 1, 5, 2, 1)

        # Descrição
        label = Gtk.Label(halign="start")
        label.set_label("Descrição do produto:*")

        scrolledwindow = Gtk.ScrolledWindow(width_request=400, height_request=200)

        description = Gtk.TextView(width_request=400, height_request=200)
        self.text = description.get_buffer()

        scrolledwindow.add(description)
        grid.attach(label, 1, 6, 1, 1)
        grid.attach(scrolledwindow, 1, 7, 2, 8)

        # Preços
        label = Gtk.Label(halign="start")
        label.set_label("Preço de venda:*")
        self.price = Gtk.Entry(max_length=10, width_request=175, halign="start")
        self.price.set_input_purpose(Gtk.InputPurpose.NUMBER)

        grid.attach(label, 3, 4, 1, 1)
        grid.attach(self.price, 3, 5, 1, 1)

        label = Gtk.Label(halign="start")
        label.set_label("Preço de custo:")
        self.costPrice = Gtk.Entry(max_length=10, width_request=175, halign="start")
        self.costPrice.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.costPrice.set_text("0")

        grid.attach(label, 3, 6, 1, 1)
        grid.attach(self.costPrice, 3, 7, 1, 1)

        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 3, 8, 1, 1)
        
        # Estoque
        label = Gtk.Label(halign="start")
        label.set_label("Estoque:")
        self.stock = Gtk.Entry(max_length=10)
        self.stock.set_text("0")

        grid.attach(label, 3, 9, 1, 1)
        grid.attach(self.stock, 3, 10, 1, 1)

        # Desconto
        label = Gtk.Label(label="Desconto de aniversário:\r(porcentagem)", halign="start")
        self.discount = Gtk.Entry(max_length=2)
        self.discount.set_text("3")
        self.discount.set_input_purpose(Gtk.InputPurpose.NUMBER)
        grid.attach(label, 3, 11, 1, 1)
        grid.attach(self.discount, 3, 12, 1, 1)

        # Foto
        label = Gtk.Label(halign="start")
        label.set_label("Selecionar imagem:*")
        self.selectFile = Gtk.FileChooserButton(title="Inserir foto")
        filefilter = Gtk.FileFilter()
        filefilter.set_name("Images")
        filefilter.add_pattern("*.png")
        filefilter.add_pattern("*.jpg")
        filefilter.add_pattern("*.jpeg")
        filefilter.add_pattern("*.bmp")
        self.selectFile.add_filter(filefilter)
        self.selectFile.connect("file-set", self.file_changed)
        grid.attach(label, 1, 15, 1, 1)
        grid.attach(self.selectFile, 1, 16, 3, 1)

        # Enviar
        enviar = Gtk.Button(margin_top=20, height_request=40)
        if not update:
            enviar.set_label("Enviar")
            enviar.connect("clicked", self.commit_product)
        else:
            self.set_ui_update_product(data)
            enviar.set_label("Atualizar (etapa 2)")
            enviar.connect("clicked", self.update_product)
        grid.attach(enviar, 1, 17, 2, 1)

        # Cancelar
        button = Gtk.Button(margin_top=20, height_request=40)
        if not update:
            button.set_label("Cancelar")
            button.connect("clicked", self.cancel_commit_product)
        else:
            button.set_label("Fechar")
            button.connect("clicked", self.cancel_update_product)
        grid.attach(button, 3, 17, 1, 1)

    def file_changed(self, widget):
        print("File selected: %s" % self.selectFile.get_filename())
    
    def simple_remove_letters(self, text):
        text = text.replace(",", "")
        text = text.replace(".", "")
        return text
    
    def cancel_commit_product(self, widget):
        submit = SbProductInsert(self.idProduct)
        submit.delete_meta_product()
        return self.destroy()
    
    def cancel_update_product(self, widget):
        return self.destroy()
    
    def commit_product(self, widget):
        barcode = self.barcode.get_text().strip()
        if len(barcode)>0:
            if not barcode.isnumeric():
                return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
            check = SbProducts()
            if check.check_product_barcode(barcode):
                return UiDialog("Erro ao enviar dados", "O código de barras informado já está cadastrado!")
        if len(self.name.get_text())<=1:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        price = self.price.get_text().strip()
        price = price.replace(",", ".")
        if not self.simple_remove_letters(price).isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        cost = self.costPrice.get_text().strip()
        cost = cost.replace(",", ".")
        if not self.simple_remove_letters(cost).isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if not self.stock.get_text().isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if not self.discount.get_text().isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if not self.selectFile.get_filename():
            return UiDialog("Entrada inválida", "Nenhuma imagem foi selecionada.")
        enviar = SbProductInsert(self.idProduct)
        if not enviar.insert_product(self.name.get_text(), barcode, self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter(), True), price, cost, self.selectFile.get_filename(), self.stock.get_text(), self.discount.get_text()):
            self.destroy()
            enviar.delete_meta_product()
            return UiDialog("Erro ao enviar dados", "Erro ao enviar dados. Por favor, tente novamente.")
        return self.destroy()

    def update_product(self, widget):
        barcode = self.barcode.get_text().strip()
        if len(barcode)>0:
            if not barcode.isnumeric():
                return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
            check = SbProducts()
            if check.check_product_barcode(barcode):
                return UiDialog("Erro ao enviar dados", "O código de barras informado já está cadastrado!")
        if len(self.name.get_text())<=1:
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        price = self.price.get_text().strip()
        price = price.replace(",", ".")
        if not self.simple_remove_letters(price).isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        cost = self.costPrice.get_text().strip()
        cost = cost.replace(",", ".")
        if not self.simple_remove_letters(cost).isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if not self.stock.get_text().isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        if not self.discount.get_text().isnumeric():
            return UiDialog("Entrada inválida", "Por favor preencha os campos corretamente.")
        img = self.selectFile.get_filename()
        if not img:
            img = False
        enviar = SbProductUpdate(self.idProduct)
        if not enviar.update_product_s2(self.name.get_text(), barcode, self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter(), True), price, cost, img, self.stock.get_text(), self.discount.get_text()):
            self.destroy()
            return UiDialog("Erro ao enviar dados", "Erro ao enviar dados. Por favor, tente novamente.")
        return self.destroy()
    
    def set_ui_update_product(self, data):
        self.barcode.set_text(str(data['data'][1]))
        self.name.set_text(str(data['data'][2]))
        self.text.set_text(str(data['data'][4]))
        self.price.set_text(str(data['data'][5]))
        self.costPrice.set_text(str(data['data'][6]))
        self.discount.set_text(str(data['data'][7]))
        self.stock.set_text(str(data['data'][8]))