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
from gi.repository import Gtk, Gdk, Pango
from gi.repository.GdkPixbuf import Pixbuf
from sysbar.ui.products import UiInfoProduct
from sysbar.lib.products import SbProducts
class UiBuy(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Lista de pedidos - SysBar", window_position="center")
        self.maximize()
        self.set_default_size(1000, 800)

        grid = Gtk.Grid(margin=10)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        treeview = Gtk.TreeView()
        # treeview.set_model(self.liststore)
        treeview.set_search_column(2)
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        # treeview.connect("row-activated", self.on_row_activated)

        scrolledwindow = Gtk.ScrolledWindow(width_request=300)
        scrolledwindow.add(treeview)
        grid.attach(scrolledwindow, 1, 1, 4, 12)

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

        treeviewcolumn = Gtk.TreeViewColumn("Quantidade")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 3)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Preço")
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 4)
        treeview.append_column(treeviewcolumn)
        
        # Valor total
        self.price = Gtk.Label(margin=10, halign="start")
        self.price.set_markup("<span size='24000'>TOTAL: </span><span size='30000' color='red'>R$0,00</span>")
        grid.attach(self.price, 1, 13, 4, 1)

        # Finalizar
        button = Gtk.Button(label="PAGAR CONTA", halign="end", width_request=140, height_request=60)
        grid.attach(button, 4, 13, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(separator, 5, 1, 1, 14)

        # Título
        label = Gtk.Label()
        label.set_markup("<span size='30000' color='red'>CAIXA ABERTO</span>")
        grid.attach(label, 6, 1, 2, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 6, 2, 2, 1)

        label = Gtk.Label(halign="start")
        label.set_markup("<span size='14000'>CLIENTE: </span><span size='16000' color='blue'>{}</span>".format("Gabriel Lasaro"))
        grid.attach(label, 6, 3, 2, 1)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 6, 4, 2, 1)

        # Notebook
        notebook = Gtk.Notebook()
        grid.attach(notebook, 6, 5, 2, 7)

        pGrid = Gtk.Grid(margin=10)
        pGrid.set_row_spacing(10)
        pGrid.set_column_spacing(10)
        subGrid2 = Gtk.Grid()
        notebook.append_page(pGrid, Gtk.Label('Código'))
        notebook.append_page(subGrid2, Gtk.Label('Lista de produtos'))

        # Produto
        pix = Pixbuf.new_from_file_at_size("icon/perfil-sysbar.svg", 320, 220)
        self.img = Gtk.Image(halign="center")
        self.img.set_from_pixbuf(pix)
        pGrid.attach(self.img, 1, 1, 2, 4)

        label = Gtk.Label(label="CÓDIGO:", halign="start")
        self.codebar = Gtk.Entry(max_length=14)
        self.codebar.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.codebar.modify_font(Pango.FontDescription('22'))
        self.codebar.connect("changed", self.search_product)
        pGrid.attach(label, 1, 5, 2, 1)
        pGrid.attach(self.codebar, 1, 6, 1, 1)

        label = Gtk.Label(label="QUANTIDADE:", halign="start")
        self.quant = Gtk.Entry()
        self.quant.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.quant.set_text("1")
        self.quant.modify_font(Pango.FontDescription('22'))
        pGrid.attach(label, 2, 5, 1, 1)
        pGrid.attach(self.quant, 2, 6, 1, 1)
        
        self.lName = Gtk.Label(halign="start")
        self.lName.set_markup("<span size='20000' color='red'>NOME DO PRODUTO...</span>")
        pGrid.attach(self.lName, 1, 7, 2, 1)

        self.lPrice = Gtk.Label(halign="start")
        self.lPrice.set_markup("<span size='12000'>VALOR UNITÁRIO: </span><span size='18000' color='blue'>R$0,00</span>")
        pGrid.attach(self.lPrice, 1, 8, 2, 1)
        
        button = Gtk.Button(label="ADICIONAR", height_request=60)
        button.connect("clicked", self.add_product)
        pGrid.attach(button, 1, 9, 1, 1)

        self.preProduct = None
        button = Gtk.Button(label="INFORMAÇÕES", height_request=60)
        button.connect("clicked", self.show_info_product)
        pGrid.attach(button, 2, 9, 1, 1)
    
    def search_product(self, widget):
        code = widget.get_text()
        if len(code)==4:
            self.preProduct = None
            result = SbProducts(code)
            data = result.search_product()
            if data['rStatus']==1:
                self.preProduct = data['data'][0]
                name = self.limit_string(data['data'][2]).upper()

                imgName = "static/{}".format(data['data'][3])
                pix = Pixbuf.new_from_file_at_size(imgName, 320, 220)
                self.img.set_from_pixbuf(pix)

                self.lName.set_markup("<span size='20000' color='red'>{}</span>".format(name))
                self.lPrice.set_markup("<span size='12000'>VALOR UNITÁRIO: </span><span size='18000' color='blue'>R${}</span>".format(str(data['data'][4]).replace(".", ',')))
                widget.set_text("")
        elif len(code)>=10:
            self.preProduct = None            
            result = SbProducts()
            data = result.search_product(code)
            if data['rStatus']==1:
                self.preProduct = data['data'][0]                
                name = self.limit_string(data['data'][2]).upper()

                imgName = "static/{}".format(data['data'][3])
                pix = Pixbuf.new_from_file_at_size(imgName, 320, 220)
                self.img.set_from_pixbuf(pix)
                
                self.lName.set_markup("<span size='20000' color='red'>{}</span>".format(name))
                self.lPrice.set_markup("<span size='12000'>VALOR UNITÁRIO: </span><span size='18000' color='blue'>R${}</span>".format(str(data['data'][4]).replace(".", ",")))
                widget.set_text("")                
    
    def limit_string(self, txt):
        if len(txt)>25:
            return "{}...".format(txt[:25].strip())
        return txt
    
    def show_info_product(self, widget):
        win = UiInfoProduct(self.preProduct)
        win.show_all()
    
    def add_product(self, widget):
        print("Add product")