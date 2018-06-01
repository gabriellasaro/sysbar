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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
class UiUpdate(Gtk.Window):

    def __init__(self, data):
        Gtk.Window.__init__(self, title="Atualizações", window_position="center")
        self.set_resizable(False)

        grid = Gtk.Grid(margin=40)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)

        # Título
        label = Gtk.Label(margin_bottom=20, halign="center")
        label.set_markup("<span size='20000' color='#68b723' font='bold'>ATUALIZAÇÃO DISPONÍVEL</span>")
        grid.attach(label, 1, 1, 1, 1)

        label = Gtk.Label()
        label.set_markup("<span color='#0d52bf'>NOVA VERSÃO: {}</span> | <span color='#c6262e'>VERSÃO INSTALADA: {}</span>".format(data[1], data[0]))
        grid.attach(label, 1, 2, 1, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=20, margin_bottom=20)
        grid.attach(separator, 1, 3, 1, 1)

        label = Gtk.Label()
        label.set_markup("<span color='#f37329'>Entre em contato com o suporte para iniciar o processo de atualização.</span>")
        grid.attach(label, 1, 4, 1, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=20, margin_bottom=20)
        grid.attach(separator, 1, 5, 1, 1)

        label = Gtk.Label()
        label.set_markup("WhatsApp: <span color='#3689e6'>(27) 37434062</span> | E-mail: <span color='#3689e6'>contato@sysbar.info</span>")
        grid.attach(label, 1, 6, 1, 1)