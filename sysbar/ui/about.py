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

class AboutSystem():

    def about_dialog(self, widget):
        about = Gtk.AboutDialog()
        about.set_transient_for(Gtk.Window())
        pix = Pixbuf.new_from_file_at_size("icon/logo.svg", 260, 140)
        about.set_logo(pix)
        about.set_program_name("SysBar")
        about.set_version("0.1")
        about.set_website("https://www.sysbar.com.br/")
        about.set_website_label("SysBar Delivery")
        about.set_comments("Sistema de gerenciamento de bares e lanchonetes.")
        about.set_authors(["Gabriel Lasaro", "Samuel Tessaro"])
        about.set_copyright("© COPYRIGHT 2018 SysBar")
        about.run()
        about.destroy()
