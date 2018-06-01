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
from sysbar.core.products.products import SbProducts
from sysbar.core.products.category import SbCategory
from sysbar.lib.session import SbSession
from sysbar.ui.dialog import UiDialog
from sysbar.ui.products.new import UiNewProduct, UiNextS2, UiNextS3, UiNextS4, UiDiscount
from sysbar.ui.products.category import UiNewCategory
class UiListProducts(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Lista de produtos - SysBar", window_position="center")
        self.set_default_size(1200, 800)
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Produtos:</span>")
        grid.attach(label, 1, 1, 1, 1)

        data = SbProducts().get_product_list()
        # Lista
        self.liststore = Gtk.ListStore(int, str, str, str, str)
        # ID - BARCODE - NAME - PRICE - STOCK
        if data['rStatus']==1:
            for item in data['data']:
                price = "R$ {}".format(str(item[3]).replace(".", ","))
                if item[5]==0:
                    self.liststore.append([item[0], str(item[1]), item[2], price, "-"])
                else:
                    self.liststore.append([item[0], str(item[1]), item[2], price, str(item[5])])
        
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

        treeviewcolumn = Gtk.TreeViewColumn("Estoque")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 4)
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
        data = SbCategory()
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
    

class UiInfoProduct(Gtk.Window):
    
    def __init__(self, idProduct):
        Gtk.Window.__init__(self, title="Informações do produto - SysBar", window_position="center")
        self.set_resizable(False)

        data = SbProducts(idProduct).get_product_info()
        if data['rStatus']==0:
            UiDialog("Não encontrado!", "Não encontramos o produto.")
            return self.destroy()
        
        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Lado esquerdo
        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Informações do produto</span>")
        grid.attach(label, 1, 1, 5, 1)

        # Nome do produto
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Nome:</span> <span color='blue'>{}</span>".format(data['data']['name']))
        grid.attach(label, 1, 2, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 1, 3, 2, 1)

        # Descrição
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Descrição:</span>")

        scrolledwindow = Gtk.ScrolledWindow(width_request=200, height_request=50)

        description = Gtk.TextView(width_request=200, height_request=50)
        description.set_editable(False)
        description.set_cursor_visible(False)
        text = description.get_buffer()
        if data['data']['description']:
            text.set_text(str(data['data']['description']))
        
        scrolledwindow.add(description)
        grid.attach(label, 1, 4, 2, 1)
        grid.attach(scrolledwindow, 1, 5, 2, 5)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 1, 10, 2, 1)

        # Ingredientes
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Ingredientes:</span>")

        scrolledwindow = Gtk.ScrolledWindow(width_request=200, height_request=50)

        ingre = Gtk.TextView(width_request=200, height_request=50)
        ingre.set_editable(False)
        ingre.set_cursor_visible(False)
        text2 = ingre.get_buffer()
        if data['data']['ingre']:
            text2.set_text(str(data['data']['ingre']))
                
        scrolledwindow.add(ingre)
        grid.attach(label, 1, 11, 2, 1)
        grid.attach(scrolledwindow, 1, 12, 2, 4)

        # Meio
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(separator, 3, 2, 1, 14)

        # Lado direito
        # ID do produto
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>ID do produto:</span> <span color='blue'>{}</span>".format(data['data']['id']))
        grid.attach(label, 4, 2, 2, 1)

        # Código de barras
        label = Gtk.Label(halign="start")
        if not data['data']['barcode']:
            label.set_markup("<span font='bold'>Código de Barras:</span> <span color='red'>Não informado.</span>")
        else:
            label.set_markup("<span font='bold'>Código de Barras:</span> <span color='blue'>{}</span>".format(data['data']['barcode']))
        grid.attach(label, 4, 3, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 4, 4, 2, 1)

        # Unidade
        label = Gtk.Label(halign="start")
        if data['data']['unity'] in ['P', 'M', 'G']:
            if data['data']['unity']=='P':
                label.set_markup("<span font='bold'>Tamanho:</span> <span color='blue'>Pequeno (P)</span>")
            elif  data['data']['unity']=='M':
                label.set_markup("<span font='bold'>Tamanho:</span> <span color='blue'>Médio (M)</span>")
            else:
                label.set_markup("<span font='bold'>Tamanho:</span> <span color='blue'>Grande (G)</span>")
        elif data['data']['unity'] in ['Kg', 'g']:
            label.set_markup("<span font='bold'>Peso:</span> <span color='blue'>{} {}</span>".format(data['data']['amount'], data['data']['unity']))
        else:
            label.set_markup("<span font='bold'>Volume:</span> <span color='blue'>{} {}</span>".format(data['data']['amount'], data['data']['unity']))
        grid.attach(label, 4, 5, 2, 1)

        # Pessoas servidas
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Pessoas servidas:</span> <span color='blue'>{}</span>".format(data['data']['peopleServed']))
        grid.attach(label, 4, 6, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 4, 7, 2, 1)

        # Estoque
        label = Gtk.Label(halign="start")
        if data['data']['statusStock']==1:
            label.set_markup("<span font='bold'>Estoque:</span> <span color='blue'>{} unidades</span>".format(data['data']['stock']))
        else:
            label.set_markup("<span font='bold'>Estoque:</span> <span color='blue'>ilimitado</span>")
        grid.attach(label, 4, 8, 2, 1)
            
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 4, 9, 2, 1)

        # Preço de venda
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Preço de Venda:</span> <span color='blue'>R$ {}</span>".format(str(data['data']['price']).replace(".", ",")))
        grid.attach(label, 4, 10, 2, 1)
        
        # Preço de custo
        button = Gtk.Button(label="Mostrar preço de custo", halign="start")
        button.connect("clicked", self.show_cust_price)
        grid.attach(button, 4, 11, 2, 1)

        self.popover = Gtk.Popover()
        self.popover.set_position(Gtk.PositionType.TOP)
        self.popover.set_relative_to(button)

        box = Gtk.Box()
        box.set_spacing(5)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        self.popover.add(box)

        label = Gtk.Label(margin=10)
        if SbSession().check_level()>=2:
            label.set_markup("<span font='bold'>Preço de custo:</span> <span color='blue'>R$ {}</span>".format(str(data['data']['custPrice']).replace(".", ",")))
        else:
            label.set_markup("<span color='red'>Você não tem permissão para ver o preço de custo.</span>")
        box.add(label)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 4, 12, 2, 1)

        # Desconto
        label = Gtk.Label(halign="start")
        free = json.loads(data['data']['discount'])
        if free['free']=='0':
            label.set_markup("<span font='bold'>Desconto:</span> <span color='red'>Desativado</span>")
        else:
            if free['type']=="percent":
                label.set_markup("<span font='bold'>Desconto:</span> <span color='blue'>A cada {} produto(s) o cliente ganha {}% de desconto.</span>".format(free['quant'], free['free']))
            elif free['type']=="money":
                label.set_markup("<span font='bold'>Desconto:</span> <span color='blue'>A cada {} produto(s) o cliente ganha R$ {} de desconto.</span>".format(free['quant'], free['free']))
            else:
                label.set_markup("<span font='bold'>Desconto:</span> <span color='blue'>A cada {} produto(s) o cliente ganha {} unidade(s) de desconto.</span>".format(free['quant'], free['free']))
        grid.attach(label, 4, 13, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 4, 14, 2, 1)

        # Categoria
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Categoria:</span> <span color='blue'>{}</span>".format(data['data']['category']))
        grid.attach(label, 4, 15, 2, 1)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 16, 5, 1)

        button = Gtk.Button(label="Alterar nome e descrições", height_request=40)
        button.connect("clicked", self.update_name, [data['data']['id'], data['data']['name'], data['data']['description'], data['data']['ingre']])
        grid.attach(button, 1, 17, 1, 1)

        button = Gtk.Button(label="Alterar código de barras", height_request=40)
        button.connect("clicked", self.update_barcode, [data['data']['id'], data['data']['barcode']])
        grid.attach(button, 2, 17, 1, 1)

        button = Gtk.Button(label="Alterar preço/estoque", height_request=40)
        button.connect("clicked", self.update_price, [data['data']['id'], data['data']['price'], data['data']['custPrice'], data['data']['stock']])
        grid.attach(button, 4, 17, 1, 1)

        button = Gtk.Button(label="Alterar desconto", height_request=40)
        button.connect("clicked", self.update_discount, [data['data']['id'], free])
        grid.attach(button, 5, 17, 1, 1)

        button = Gtk.Button(label="Alterar informações tecnicas", height_request=40)
        button.connect("clicked", self.update_technical_information, [data['data']['id'], data['data']['unity'], data['data']['amount'], data['data']['peopleServed'], data['data']['virtualMenu'], data['data']['delivery'], data['data']['specialRequest'], data['data']['idCategory']])
        grid.attach(button, 4, 18, 2, 1)

        button = Gtk.Button(label="Atualizar", height_request=40)
        button.connect("clicked", self.show_info_product, idProduct)
        grid.attach(button, 4, 19, 1, 1)
        
        button = Gtk.Button(label="Fechar", height_request=40)
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 5, 19, 1, 1)

        label = Gtk.Label()
        label.set_markup("<span font='bold'>Registrado em:</span> {}".format(data['data']['register'][:-7]))
        grid.attach(label, 1, 18, 2, 1)

        label = Gtk.Label()
        if not data['data']['lastChange']:
            label.set_markup("<span font='bold'>Última alteração:</span> nunca sofreu alteração.")
        else:
            label.set_markup("<span font='bold'>Última alteração:</span> {}".format(data['data']['lastChange'][:-7]))
        grid.attach(label, 1, 19, 2, 1)

    def show_info_product(self, widget, idProduct):
        self.destroy()
        win = UiInfoProduct(idProduct)
        win.show_all()

    def update_barcode(self, widget, data):
        win = UiNewProduct(data, True)
        win.show_all()
    
    def update_name(self, widget, data):
        win = UiNextS2(data, True)
        win.show_all()
    
    def update_price(self, widget, data):
        win = UiNextS3(data, True)
        win.show_all()
    
    def update_technical_information(self, widget, data):
        win = UiNextS4(data, True)
        win.show_all()
    
    def update_discount(self, widget, data):
        win = UiDiscount(data, True)
        win.show_all()
    
    def show_cust_price(self, widget):
        self.popover.show_all()
    
    def destroy_window(self, widget):
        self.destroy()