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
import requests, json
from sysbar.ui.update import UiUpdate

request = requests.get("https://www.sysbar.info/version.json")
if request.status_code==200:
    data = request.json()
    if data['version']>"0.1":
        print("Atualização disponível! (Nova versão: {} - Versão instalada: {})".format(data['version'], "0.1"))
        print("Entre em contato com o suporte.")
        win = UiUpdate(["0.1", data['version']])
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()