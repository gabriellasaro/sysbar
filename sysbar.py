#!/usr/bin/python3
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
import gi, json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from sysbar.ui.box import UiBox
from sysbar.ui.dialog import UiDialog
from sysbar.lib.settings import SbTheme
from sysbar.lib.session import SbLogin
import subprocess
class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Entrar - SysBar", window_position="center", modal=True, icon_name="system-lock-screen")
        self.set_resizable(False)

        # Ativa o tema escolhido.
        self.active_theme()

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=60, halign="center", valign="center")
        self.add(self.box)

        self.pix = Pixbuf.new_from_file_at_size("icon/logo.svg", 220, 120)
        self.img1 = Gtk.Image()
        self.img1.set_from_pixbuf(self.pix)
        self.box.pack_start(self.img1, True, True, 0)

        self.label = Gtk.Label(label="Username:", margin_top=10)
        self.box.pack_start(self.label, True, True, 0)

        self.username = Gtk.Entry(max_length=120, input_purpose="alpha")
        # Valor predefinido no campo.
        self.username.set_text(self.select_last_user())
        self.box.pack_start(self.username, True, True, 0)

        self.label = Gtk.Label("PIN:")
        self.box.pack_start(self.label, True, True, 0)

        self.pin = Gtk.Entry(max_length=120, input_purpose="password", visibility=False, activates_default=True)
        # Valor predefinido no campo.
        self.pin.set_text('1234')
        self.pin.connect("activate", self.on_button1_clicked)
        self.box.pack_start(self.pin, True, True, 0)

        self.button = Gtk.Button(label="Entrar", margin_top=5, height_request=40)
        self.button.connect("clicked", self.on_button1_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.spinner = Gtk.Spinner(margin=10)
        self.box.pack_start(self.spinner, True, True, 0)

        self.label = Gtk.Label("© COPYRIGHT 2018 SysBar")
        self.box.pack_start(self.label, True, True, 0)

    def on_button1_clicked(self, widget):
        self.spinner.start()
        username = self.username.get_text().strip()
        pin = self.pin.get_text().strip()
        if not username:
            self.spinner.stop()            
            return UiDialog('Atenção', 'Dados de entrada inválidos.')
        if not pin:
            self.spinner.stop()            
            return UiDialog('Atenção', 'Dados de entrada inválidos.')
        login = SbLogin(username, pin)
        if login.get_status()['rStatus']=='1':
            print("Conectou-se com o usuário: {}".format(username))
            self.spinner.stop()
            win2 = UiBox()
            win2.connect("delete-event", Gtk.main_quit)
            win2.show_all()
            win.destroy()
            self.save_last_user(username)
        elif login.get_status()['rStatus']=='10':
            self.spinner.stop()
            return UiDialog('Atenção', 'Este usuário está desativado.')
        elif login.get_status()['rStatus']=='4':
            self.spinner.stop()
            return UiDialog('Atenção', 'Usuário ou senha incorreto.')
        elif login.get_status()['rStatus']=='3':
            self.spinner.stop()
            return UiDialog('Atenção', 'Usuário não encontrado.')
        else:
            self.spinner.stop()
            return UiDialog('Atenção', 'Erro desconhecido.')
        
    def select_last_user(self):
        try:
            data = open('/home/gabriel/.system-bar/last-user.txt', 'r')
            user = data.read()
            data.close()
            return user.strip()
        except:
            return ""

    def save_last_user(self, user):
        write = open('/home/gabriel/.system-bar/last-user.txt','w+')
        write.write(user)
        write.close()
    
    def active_theme(self):
        theme = SbTheme()
        if not theme.get_theme():
            return 0
        else:
            css = open('theme/sysbar-lite.css', 'r')
            style_provider = Gtk.CssProvider()
            style_provider.load_from_data(bytes(css.read(), 'UTF-8'))
            css.close()
            
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
subprocess.Popen('./update.py')
win = Window()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()