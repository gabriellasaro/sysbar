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
from sysbar.ui.dialog import UiDialog
from sysbar.lib.tables import SbTables
from sysbar.lib.session import SbSession
class UiTableList(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Lista de mesas", window_position="center")
        self.set_default_size(800, 600)

        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Mesas:</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Lista
        self.liststore = Gtk.ListStore(int, str, str, int)
        # ID - PRICE - BUSY - CAPACIDADE
        data = SbTables()
        rData = data.get_tables_list()
        if rData['rStatus']==1:
            for table in rData['data']:
                price = "R$ {}".format(str(table[1]).replace('.', ','))
                if table[2]==0:
                    self.liststore.append([table[0], price, "Disponível", table[3]])
                else:
                    self.liststore.append([table[0], price, "Ocupada", table[3]])
        
        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        treeview.set_search_column(2)
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        # treeview.connect("row-activated", self.on_row_activated)

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

        treeviewcolumn = Gtk.TreeViewColumn("Preço da mesa")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Status")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 2)
        treeview.append_column(treeviewcolumn)

        treeviewcolumn = Gtk.TreeViewColumn("Capacidade")
        treeviewcolumn.set_spacing(10)
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, False)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 3)
        treeview.append_column(treeviewcolumn)

        button = Gtk.Button(label="Adicionar mesa", height_request=40, halign="start")
        button.connect("clicked", self.show_new_table)
        grid.attach(button, 1, 3, 1, 1)

        button = Gtk.Button(label="Atualizar", height_request=40, halign="end")
        button.connect("clicked", self.update_list)
        grid.attach(button, 2, 3, 1, 1)
    
    def update_list(self, widget):
        self.liststore.clear()
        data = SbTables()
        rData = data.get_tables_list()
        if rData['rStatus']==1:
            for table in rData['data']:
                price = "R$ {}".format(str(table[1]).replace('.', ','))
                if table[2]==0:
                    self.liststore.append([table[0], price, "Disponível", table[3]])
                else:
                    self.liststore.append([table[0], price, "Ocupada", table[3]])
    
    def show_new_table(self, widget):
        win = UiNewTable()
        win.show_all()
    
class UiNewTable(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Adicionar mesa", window_position="center")
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
        label = Gtk.Label(margin_bottom=30)
        label.set_markup("<span size='20000'>Adicionar mesa</span>")
        grid.attach(label, 1, 1, 1, 1)

        # Número da mesa
        label = Gtk.Label(halign="start")
        label.set_label("Número da mesa:")
        self.tableId = Gtk.Entry()
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.tableId, 1, 3, 1, 1)

        # Preço
        label = Gtk.Label(halign="start")
        label.set_label("Preço:")
        self.price = Gtk.Entry()
        self.price.set_text("0")
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.price, 1, 5, 1, 1)

        # Capacidade
        label = Gtk.Label(halign="start")
        label.set_label("Capacidade: (pessoas)")
        self.capacity = Gtk.Entry(max_length=4)
        self.capacity.set_text("2")
        grid.attach(label, 1, 6, 1, 1)
        grid.attach(self.capacity, 1, 7, 1, 1)

        # Enviar
        button = Gtk.Button(label="Enviar", height_request=40)
        grid.attach(button, 1, 8, 1, 1)