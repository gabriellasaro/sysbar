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
from escpos import *
class SbPrinterComanda():
    
    def __init__(self, order):
        try:
            self.printer = printer.Usb(0x0456, 0x0808, 3, 0x02, 0x03)
            self._start(order)
        except:
            print("Sem conexão com a impressora.")

    def _start(self, args):
        self.printer.set(align='center', font='a')
        self.printer.text("--------------------------------\n")
        self.printer.text("COMANDA: {}\n".format(args['ID_comanda']))
        self.printer.set(align='left')
        self.printer.text("Mesa: {}\n".format(args['ID_table']))
        self.printer.set(font='b')
        self.printer.text("Cliente: {}\n".format(args['client_name']))
        self.printer.text("\n")
        self.printer.set(align='left')
        self.printer.text("ITENS:\n")
        self.printer.set(align='left', font='a')
        for x in args['printer']:
            self.printer.text("{} - {}x Und. - {}\n".format(x['ID_product'], x['amount'], x['name']))
            if x['comment']:
                self.printer.text("Obs: {}\n".format(x['comment']))
                self.printer.text("----\n")
        self.printer.text("\n")
        # self.printer.barcode(args[0], 'CODE128', 64, 2, '', '', align_ct=True, function_type='B')
        self.printer.set(align='center', font='a')
        self.printer.text("--------------------------------\n")
        self.printer.text("\n")
        self.printer.cut()