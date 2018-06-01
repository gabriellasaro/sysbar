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
from sysbar.lib.session import SbSession
from sysbar.ui.dialog import UiDialog
from sysbar.core.products.category import SbCategory
class UiNewCategory(Gtk.Window):

    def __init__(self, update=False, categoryId=None, name=None):
        Gtk.Window.__init__(self, window_position="center")
        self.set_resizable(False)
        
        userLevel = SbSession()
        if userLevel.check_level()!=3:
            UiDialog("Erro de permissão", "Este usuário não possui permissão para acessar as informações.")
            return self.destroy()
        
        grid = Gtk.Grid(margin=40)
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Título
        if update:
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
        name = self.name.get_text().strip()
        if not name:
            return UiDialog("Entrada inválida", "Por favor preencha o campo corretamente.")
        self.destroy()
        submit = SbCategory(categoryId)
        if not submit.update_category(name):
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")
    
    def submit_category(self, widget):
        name = self.name.get_text().strip()
        if not name:
            return UiDialog("Entrada inválida", "Por favor preencha o campo corretamente.")
        self.destroy()
        submit = SbCategory()
        if not submit.insert_category(name):
            return UiDialog("Erro ao enviar dados", "Erro ao inserir informações no banco de dados.")