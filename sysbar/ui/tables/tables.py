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
from sysbar.lib.session import SbSession
from sysbar.core.tables.tables import SbTables, SbNewTable
class UiTableList(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Lista de mesas", window_position="center")
        self.set_default_size(900, 700)

        grid = Gtk.Grid(margin=20)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30, halign="start")
        label.set_markup("<span size='20000'>Mesas:</span>")
        grid.attach(label, 1, 1, 4, 1)

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
        treeview.connect("row-activated", self.show_info_table)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(treeview)
        grid.attach(scrolledwindow, 1, 2, 4, 1)

        cellrenderertext = Gtk.CellRendererText()
        
        treeviewcolumn = Gtk.TreeViewColumn("Número")
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
        grid.attach(button, 4, 3, 1, 1)

    def show_info_table(self, widget, treepath, text):
        win = UiNewTable([self.liststore[treepath][0], self.liststore[treepath][1][3:], self.liststore[treepath][3]], True)
        win.show_all()
        
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

    def __init__(self, data=None, update=False):
        Gtk.Window.__init__(self, window_position="center")
        self.set_resizable(False)
        userLevel = SbSession()
        if userLevel.check_level()<2:
            UiDialog("Erro de permissão", "Este usuário não possui permissão para acessar as informações.")
            return self.destroy()

        grid = Gtk.Grid(margin=30)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=30)
        if not update:
            label.set_markup("<span size='20000'>Adicionar mesa</span>")
            self.set_title("Adicionar mesa")
        else:
            label.set_markup("<span size='20000'>Atualizar mesa</span>")
            self.set_title("Atualizar mesa")
        grid.attach(label, 1, 1, 1, 1)

        # Número da mesa
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Número da mesa:</span><span color='red'>*</span>")
        self.tableId = Gtk.Entry()
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.tableId, 1, 3, 1, 1)

        # Preço
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Preço:</span>")
        self.price = Gtk.Entry()
        self.price.set_text("0")
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.price, 1, 5, 1, 1)

        # Capacidade
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Capacidade:</span> (pessoas)")
        self.capacity = Gtk.Entry(max_length=6)
        self.capacity.set_text("4")
        grid.attach(label, 1, 6, 1, 1)
        grid.attach(self.capacity, 1, 7, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 8, 1, 1)

        # Enviar
        button = Gtk.Button(height_request=40)
        if not update:
            button.set_label("Enviar")
            button.connect("clicked", self.submit)
        else:
            button.set_label("Atualizar")
            button.connect("clicked", self.update, data[0])
            self.tableId.set_text(str(data[0]))
            self.price.set_text(str(data[1]))
            self.capacity.set_text(str(data[2]))
        grid.attach(button, 1, 9, 1, 1)
    
    def submit(self, widget):
        tableId = self.tableId.get_text().strip()
        if not tableId.isnumeric():
            return UiDialog("Entrada inválida!", "Por favor, insira um número de mesa válido.")

        price = self.price.get_text().strip()
        price = price.replace(",", ".")
        if not self.simple_remove_letters(price).isnumeric():
            return UiDialog("Entrada inválida!", "Por favor, forneça um valor válido.")
        quant = self.capacity.get_text().strip()
        if not tableId.isnumeric():
            return UiDialog("Entrada inválida!", "Por favor, forneça um valor válido.")
        
        result = SbNewTable(tableId).insert_table([price, quant])
        if result['rStatus'] == 4:
            return UiDialog("Conflito!", "Já existe um mesa cadastrada com esse número.")
        if result['rStatus'] == 0:
            return UiDialog("Erro ao enviar!", "Não foi possível enviar as informações.")
        return self.destroy()
    
    def update(self, widget, tableId):
        newId = self.tableId.get_text().strip()
        if not newId.isnumeric():
            return UiDialog("Entrada inválida!", "Por favor, insira um número de mesa válido.")

        price = self.price.get_text().strip()
        price = price.replace(",", ".")
        if not self.simple_remove_letters(price).isnumeric():
            return UiDialog("Entrada inválida!", "Por favor, forneça um valor válido.")
        quant = self.capacity.get_text().strip()
        if not quant.isnumeric():
            return UiDialog("Entrada inválida!", "Por favor, forneça um valor válido.")
        
        result = SbNewTable(tableId).update_table([newId, price, quant])
        if result['rStatus'] == 4:
            return UiDialog("Conflito!", "Já existe um mesa cadastrada com esse número.")
        if result['rStatus'] == 0:
            return UiDialog("Erro ao enviar!", "Não foi possível enviar as informações.")
        return self.destroy()
    
    def simple_remove_letters(self, text):
        text = text.replace(",", "")
        text = text.replace(".", "")
        return text