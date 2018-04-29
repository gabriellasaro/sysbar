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
class UiDialog():
    def __init__(self, title, text):
        self.messagedialog = Gtk.MessageDialog(message_format="MessageDialog")
        self.messagedialog.set_transient_for()
        self.messagedialog.set_title(title)
        self.messagedialog.set_markup("<span size='12000'><b>{}</b></span>".format(title))
        self.messagedialog.format_secondary_text(text)
        self.messagedialog.add_button("_Fechar", Gtk.ResponseType.CLOSE)
        self.messagedialog.set_property("message-type", Gtk.MessageType.INFO)

        self.messagedialog.run()
        self.messagedialog.hide()