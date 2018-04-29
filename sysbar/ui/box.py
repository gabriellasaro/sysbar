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
import threading
from time import sleep

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, Gdk, Pango
from gi.repository.GdkPixbuf import Pixbuf
from sysbar.lib.session import SbSession, SbLogout
from sysbar.lib.client import SbClient
from sysbar.ui.about import AboutSystem
from sysbar.ui.tables import UiTableList
from sysbar.ui.admin import UiAdmin
from sysbar.ui.client import UiCustomerList, UiNewCustomer, UiCustomerInfo
from sysbar.ui.comanda import UiBuy
class UiBox(Gtk.Window):

    # def __init__(self):
    #     subprocess.Popen('./server.py')
    
    def __init__(self):
        Gtk.Window.__init__(self, title="Caixa - SysBar", window_position="center", icon_name="applications-utilities")
        self.maximize()
        # Gtk.Window.fullscreen(self)
        # self.set_default_size(900, 400)
        
        self.connect("destroy", self.logout_system)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=0)
        self.add(box)

        # Menu de ferramentas
        subBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0, margin=0)
        box.pack_start(subBox, True, True, 0)
        
        pix = Pixbuf.new_from_file_at_size("icon/gksu.svg", 60, 60)
        img = Gtk.Image()
        img.set_from_pixbuf(pix)
        button = Gtk.Button(margin=4)
        button.set_image(img)
        button.set_focus_on_click(False)
        button.connect("clicked", self.show_new_customer)

        subBox.pack_start(button, True, True, 0)

        pix = Pixbuf.new_from_file_at_size("icon/winefile.svg", 60, 60)
        img = Gtk.Image()
        img.set_from_pixbuf(pix)
        button = Gtk.Button(margin=4)
        button.add(img)
        button.set_focus_on_click(False)
        button.connect("clicked", self.show_customer_list)

        subBox.pack_start(button, True, True, 0)

        pix = Pixbuf.new_from_file_at_size("icon/fbreader.svg", 60, 60)
        img = Gtk.Image()
        img.set_from_pixbuf(pix)
        button = Gtk.Button(margin=4)
        button.add(img)
        button.set_focus_on_click(False)
        button.connect("clicked", self.show_tables_list)

        subBox.pack_start(button, True, True, 0)

        pix = Pixbuf.new_from_file_at_size("icon/preferences-desktop.png", 60, 60)
        img = Gtk.Image()
        img.set_from_pixbuf(pix)
        button = Gtk.Button(margin=4)
        button.add(img)
        button.set_focus_on_click(False)
        button.connect("clicked", self.show_ui_admin)

        subBox.pack_start(button, True, True, 0)        
        

        pix = Pixbuf.new_from_file_at_size("icon/hwinfo.svg", 60, 60)
        img = Gtk.Image()
        img.set_from_pixbuf(pix)
        button = Gtk.Button(margin=4)
        button.add(img)
        button.set_focus_on_click(False)
        wAbout = AboutSystem()
        button.connect("clicked", wAbout.about_dialog)

        subBox.pack_start(button, True, True, 0)        

        pix = Pixbuf.new_from_file_at_size("icon/gshutdown.svg", 60, 60)
        img = Gtk.Image()
        img.set_from_pixbuf(pix)
        button = Gtk.Button(margin=4)
        button.add(img)
        button.set_focus_on_click(False)
        button.connect("clicked", self.dialog_logout)

        subBox.pack_start(button, True, True, 0)

        # GRID
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        box.pack_start(grid, True, True, 0)

        # Pedido do cliente
        label = Gtk.Label(margin_left=20, margin_right=20, margin_top=30, margin_bottom=10, halign="center", valign="end")
        label.set_markup("<span size=\"40000\">NÚMERO DO CLIENTE:</span>")
        grid.attach(label, 1, 1, 1, 1)

        listPhone = Gtk.ListStore(str)
        customers = SbClient()
        data = customers.get_customer_list()
        for client in data['data']:
            listPhone.append([client[1]])

        entrycompletion = Gtk.EntryCompletion()
        entrycompletion.set_model(listPhone)
        entrycompletion.set_text_column(0)
        entrycompletion.set_inline_completion(False)

        self.idClient = Gtk.Entry(margin_left=20, margin_right=20, max_length=12, input_purpose="phone", width_request=400, halign="center", valign="start")
        self.idClient.set_completion(entrycompletion)
        self.idClient.grab_focus_without_selecting()
        self.idClient.modify_font(Pango.FontDescription('32'))
        # self.entry1.modify_font(Pango.FontDescription('Sans Serif 24'))
        # self.idClient.connect("activate", self.on_event1)
        # Valor predefinido no campo.
        # self.idClient.set_text("27996135732")
        grid.attach(self.idClient, 1, 2, 1, 1)

        
        gridBt = Gtk.Grid(halign="center", margin_top=5, margin_bottom=5)
        # gridBt.set_row_homogeneous(False)
        # gridBt.set_column_homogeneous(False)
        bt01 = Gtk.Button(label="7", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 1, 1, 1, 1)
        
        bt01 = Gtk.Button(label="8", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 2, 1, 1, 1)

        bt01 = Gtk.Button(label="9", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 3, 1, 1, 1)

        bt01 = Gtk.Button(label="4", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 1, 2, 1, 1)
        
        bt01 = Gtk.Button(label="5", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 2, 2, 1, 1)

        bt01 = Gtk.Button(label="6", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 3, 2, 1, 1)

        bt01 = Gtk.Button(label="1", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 1, 3, 1, 1)
        
        bt01 = Gtk.Button(label="2", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 2, 3, 1, 1)

        bt01 = Gtk.Button(label="3", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)        
        gridBt.attach(bt01, 3, 3, 1, 1)

        bt01 = Gtk.Button(label="0", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_button)
        gridBt.attach(bt01, 4, 1, 1, 2)

        bt01 = Gtk.Button(label="<", margin=5, width_request=70, height_request=60)
        bt01.connect("clicked", self.on_event_back)
        gridBt.attach(bt01, 4, 3, 1, 1)

        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)
        button = Gtk.Button(label="FECHAR CONTA", margin_top=10, margin_left=5, height_request=60)
        button.add_accelerator("clicked",
                               accelgroup,
                               Gdk.keyval_from_name("f"),
                               Gdk.ModifierType.CONTROL_MASK,
                               Gtk.AccelFlags.VISIBLE)
        button.connect("clicked", self.on_event1)
        button.set_focus_on_click(False)
        # button.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse("#FD0000"))
        gridBt.attach(button, 1, 4, 2, 1)

        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)
        button = Gtk.Button(label="INFORMAÇÕES", margin_top=10, margin_left=10, margin_right=5, height_request=60)
        button.add_accelerator("clicked",
                               accelgroup,
                               Gdk.keyval_from_name("i"),
                               Gdk.ModifierType.CONTROL_MASK,
                               Gtk.AccelFlags.VISIBLE)
        button.connect("clicked", self.show_customer_info)
        button.set_focus_on_click(False)
        # button.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse("#FFC90B"))
        gridBt.attach(button, 3, 4, 2, 1)

        grid.attach(gridBt, 1, 3, 1, 1)

        # Nova compra
        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)
        button = Gtk.Button(label="NOVA COMPRA", width_request=310, height_request=60, halign="center")
        button.add_accelerator("clicked",
                               accelgroup,
                               Gdk.keyval_from_name("n"),
                               Gdk.ModifierType.CONTROL_MASK,
                               Gtk.AccelFlags.VISIBLE)
        button.connect("clicked", self.on_event1)
        button.set_focus_on_click(False)
        # button.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse("#0080DB"))
        grid.attach(button, 1, 4, 1, 1)

        # Lista
        # ID - PHONE - NAME - CREDIT
        self.liststore = Gtk.ListStore(int, str, str, float)
        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        treeview.set_search_column(2)
        treeview.set_vexpand(True)
        treeview.set_hexpand(True)
        # treeview.connect("row-activated", self.on_row_activated)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(treeview)
        grid.attach(scrolledwindow, 2, 1, 1, 4)

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

        # Informações da sessão
        data = SbSession()
        session = data.get_info()
        label = Gtk.Label("Usuário: {} ({})".format(session['user']['username'], session['user']['name']), halign="center", valign="end", margin_bottom=10)
        box.pack_start(label, True, True, 0)

        # Copyright
        # label = Gtk.Label("© COPYRIGHT 2018 SysBar", ypad=18, halign="center", valign="end")
        # box.pack_start(label, True, True, 0)
        thread = threading.Thread(target=self.start_update)
        thread.daemon = True
        thread.start()
    
    def start_update(self):
        while True:
            GLib.idle_add(self.update_list)
            sleep(10)
    
    def update_list(self):
        # self.liststore.clear()
        # ID - PHONE - NAME - CREDIT
        data = SbClient()
        rData = data.get_customer_list()
        if rData['rStatus']==1:
            for client in rData['data']:
                self.liststore.append([client[0], client[1], client[2], client[3]])
    
    # Abrir janelas
    def on_event1(self, widget):
        print("Abrir comanda.")
        win = UiBuy()
        win.show_all()
    
    def show_tables_list(self, widget):
        win = UiTableList()
        win.show_all()
    
    def show_new_customer(self, widget):
        win = UiNewCustomer()
        win.show_all()
    
    def show_customer_list(self, widget):
        win = UiCustomerList()
        win.show_all()
    
    def show_customer_info(self, widget):
        win = UiCustomerInfo(self.idClient.get_text())
        win.show_all()
    
    def show_ui_admin(self, widget):
        win = UiAdmin()
        win.show_all()
    # Fim janelas
    
    def on_event_button(self, widget):
        txt = self.idClient.get_text()
        txt += widget.get_label()
        self.idClient.set_text(txt)
    
    def on_event_back(self, widget):
        self.idClient.set_text(self.idClient.get_text()[:-1])
    
    def dialog_logout(self, widget):
        dialog = Gtk.Dialog()
        dialog.set_title("Encerrar sessão?")
        dialog.set_transient_for(Gtk.Window())
        label = Gtk.Label("Deseja mesmo encerrar a sessão?", margin=40)
        dialog.vbox.add(label)
        
        dialog.add_button("_OK", Gtk.ResponseType.OK)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.connect("response", self.logout_system_dialog)

        dialog.show_all()
    
    def logout_system_dialog(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            session = SbLogout()
            print("Fechando...")
            Gtk.main_quit()
        elif response == Gtk.ResponseType.CANCEL:
            print("Finalização de sessão cancelado.")
        else:
            print("Finalização de sessão cancelado.")
        dialog.destroy()
    
    def logout_system(self, widget):
        SbLogout()
        print("Fechando...")