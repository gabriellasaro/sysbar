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
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from sysbar.core.products.category import SbCategory
from sysbar.core.products.new import SbNewProduct, SbUpdateProduct
from sysbar.lib.session import SbSession
from sysbar.ui.dialog import UiDialog

class UiNewProduct(Gtk.Window):

    def __init__(self, data=None, update=False):
        Gtk.Window.__init__(self, window_position="center")
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
        label = Gtk.Label(margin_bottom=20)
        if not update:
            self.set_title("1ª Etapa - Novo produto")
            label.set_markup("<span size='21000'>Deseja adicionar código de barras?</span>")
        else:
            self.set_title("Atualizar código de barras")
            label.set_markup("<span size='21000'>Atualizar o código de barras</span>")
        grid.attach(label, 1, 1, 2, 1)

        label = Gtk.Label()
        label.set_markup("<span font='bold'>Código de barras:</span>")
        grid.attach(label, 1, 2, 2, 1)
        self.code = Gtk.Entry(max_length=20)
        if not update:
            self.code.connect("activate", self.next_step)
        else:
            self.code.connect("activate", self.update, data[0])            
        grid.attach(self.code, 1, 3, 2, 1)

        label = Gtk.Label()
        label.set_markup("<span color='#c6262e' font='bold'>Adicionar o código de barras é opcional.</span>")
        grid.attach(label, 1, 4, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 5, 2, 1)

        button = Gtk.Button(height_request=40)
        if not update:
            button.set_label("Próximo")
            button.connect("clicked", self.next_step)
            # Define as informações
            if data:
                if data['stage']==1:
                    self.code.set_text(data['data']['code'])
        else:
            self.code.set_text(str(data[1]))
            button.set_label("Atualizar")
            button.connect("clicked", self.update, data[0])
        grid.attach(button, 1, 6, 1, 1)

        button = Gtk.Button(label="Fechar")
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 2, 6, 1, 1)
    
    def next_step(self, widget):
        code = self.code.get_text().strip()
        data = {
            'stage':1,
            'data':{
                'code':code
            }
        }
        if code:
            if SbNewProduct().check_product_barcode(code):
                return UiDialog("Conflito com dados existentes", "Um produto com este código de barras já exister. Não é possível adicionar.")
            else:
                win = UiNextS2(data)
                win.show_all()
                return self.destroy()
        else:
            win = UiNextS2(data)
            win.show_all()
            return self.destroy()
    
    def update(self, widget, idProduct):
        code = self.code.get_text().strip()
        if code:
            if SbNewProduct().check_product_barcode(code):
                return UiDialog("Conflito com dados existentes", "Um produto com este código de barras já exister. Não é possível adicionar.")
        submit = SbUpdateProduct()
        submit.set_product_id(idProduct)
        if not submit.update_barcode(code):
            return UiDialog("Erro ao enviar dados!", "Não foi possível enviar as informações para a base de dados.")
        return self.destroy()
    
    def destroy_window(self, widget):
        return self.destroy()

class UiNextS2(Gtk.Window):

    def __init__(self, data=None, update=False):
        Gtk.Window.__init__(self, window_position="center")
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
        label = Gtk.Label(margin_bottom=20, halign="start")
        if not update:
            self.set_title("2ª Etapa - Novo produto")
            label.set_markup("<span size='21000'>Descrição e Ingredientes</span>")
        else:
            self.set_title("Atualizar descrição e ingredientes")
            label.set_markup("<span size='21000'>Atualizar descrição e ingredientes</span>")
        grid.attach(label, 1, 1, 2, 1)

        # Nome do produto
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Nome do produto:</span><span color='red'>*</span>")
        self.name = Gtk.Entry(max_length=120)
        grid.attach(label, 1, 2, 2, 1)
        grid.attach(self.name, 1, 3, 2, 1)

        label = Gtk.Label(margin_top=10)
        label.set_markup("<span color='#c6262e' font='bold'>Nomes curtos e intuitivos chamão mais à atenção.</span>")
        grid.attach(label, 1, 4, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 5, 2, 1)

        # Descrição
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Descrição:</span>")

        scrolledwindow = Gtk.ScrolledWindow(width_request=400, height_request=50)

        description = Gtk.TextView(width_request=400, height_request=50)
        self.text = description.get_buffer()

        scrolledwindow.add(description)
        grid.attach(label, 1, 6, 2, 1)
        grid.attach(scrolledwindow, 1, 7, 2, 8)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 15, 2, 1)

        # Ingredientes
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Ingredientes:</span>")

        scrolledwindow = Gtk.ScrolledWindow(width_request=400, height_request=30)

        ingre = Gtk.TextView(width_request=400, height_request=30)
        self.text2 = ingre.get_buffer()

        scrolledwindow.add(ingre)
        grid.attach(label, 1, 16, 2, 1)
        grid.attach(scrolledwindow, 1, 17, 2, 8)

        label = Gtk.Label(margin_top=10)
        label.set_markup("<span color='#c6262e' font='bold'>Sempre separe os ingredientes por uma vírgula. (Ex.: tomate, milho)</span>")
        grid.attach(label, 1, 25, 2, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 26, 2, 1)

        button = Gtk.Button(height_request=40)
        if not update:
            button.set_label("Próximo")
            button.connect("clicked", self.next_step, data)
            # Define as informações
            if data['stage']>=2:
                    self.set_data(data)
            else:
                back = Gtk.Button(height_request=40, label="Voltar")
                back.connect("clicked", self.come_back, data)
                grid.attach(back, 1, 27, 1, 1)
        else:
            button.set_label("Atualizar")
            button.connect("clicked", self.update, data[0])
            self.set_data(data, True)
        
        grid.attach(button, 2, 27, 1, 1)
    
    def next_step(self, widget, data):
        name = self.name.get_text().strip()
        if name:
            if len(name)>120:
                return UiDialog("Entrada inválida", "Você excedeu o limite de 120 caracteres no nome do produto.")
            if len(name)<=6:
                return UiDialog("Entrada inválida", "Nome de produto muito curto, utilize um nome maior.")
        if not name:
            return UiDialog("Entrada inválida", "Forneça um nome para o seu produto.")
        
        description = self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter(), True).strip()
        ingre = self.text2.get_text(self.text2.get_start_iter(), self.text2.get_end_iter(), True).strip()
        if data['stage']<2:
            data['stage'] = 2
        data['data']['name'] = name
        data['data']['description'] = description
        data['data']['ingre'] = ingre

        win = UiNextS3(data)
        win.show_all()
        return self.destroy()
    
    def update(self, widget, idProduct):
        name = self.name.get_text().strip()
        if name:
            if len(name)>120:
                return UiDialog("Entrada inválida", "Você excedeu o limite de 120 caracteres no nome do produto.")
            if len(name)<=6:
                return UiDialog("Entrada inválida", "Nome de produto muito curto, utilize um nome maior.")
        if not name:
            return UiDialog("Entrada inválida", "Forneça um nome para o seu produto.")
        
        description = self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter(), True).strip()
        ingre = self.text2.get_text(self.text2.get_start_iter(), self.text2.get_end_iter(), True).strip()

        submit = SbUpdateProduct()
        submit.set_product_id(idProduct)
        if not submit.update_info([name, description, ingre]):
            return UiDialog("Erro ao enviar dados!", "Não foi possível enviar as informações para a base de dados.")
        return self.destroy()
    
    def come_back(self, widget, data):
        win = UiNewProduct(data)
        win.show_all()
        return self.destroy()
    
    def set_data(self, data, other=False):
        if not other:
            self.name.set_text(data['data']['name'])
            self.text.set_text(data['data']['description'])
            self.text2.set_text(data['data']['ingre'])
        else:
            self.name.set_text(data[1])
            if data[2]:
                self.text.set_text(str(data[2]))
            if data[3]:
                self.text2.set_text(str(data[3]))

class UiNextS3(Gtk.Window):

    def __init__(self, data=None, update=False):
        Gtk.Window.__init__(self, window_position="center")
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
        label = Gtk.Label(margin_bottom=20, halign="start")
        if not update:
            self.set_title("3ª Etapa - Novo produto")
            label.set_markup("<span size='21000'>Preço e Estoque</span>")
        else:
            self.set_title("Atualizar produto")
            label.set_markup("<span size='21000'>Atualizar preço e estoque</span>")
        grid.attach(label, 1, 1, 2, 1)

        # Preços
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Preço de venda:</span><span color='red'>*</span>")
        self.price = Gtk.Entry(max_length=10)
        self.price.set_input_purpose(Gtk.InputPurpose.NUMBER)

        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.price, 1, 3, 1, 1)

        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Preço de custo:</span>")
        self.costPrice = Gtk.Entry(max_length=10)
        self.costPrice.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.costPrice.set_text("0")

        grid.attach(label, 2, 2, 1, 1)
        grid.attach(self.costPrice, 2, 3, 1, 1)

        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 1, 4, 2, 1)
        
        # Estoque
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Estoque:</span>")
        self.stock = Gtk.Entry(max_length=10)
        self.stock.set_text("0")
        grid.attach(label, 1, 5, 1, 1)
        grid.attach(self.stock, 1, 6, 1, 1)

        label = Gtk.Label(margin_top=10)
        label.set_markup("<span color='#c6262e' font='bold'>Atenção:</span> o produto que não\rpossue estoque definido, deve\rser deixado em branco ou (0).")
        grid.attach(label, 2, 5, 1, 2)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 8, 2, 1)

        button = Gtk.Button(height_request=40)
        if not update:
            button.set_label("Próximo")
            button.connect("clicked", self.next_step, data)
            back = Gtk.Button(height_request=40, label="Voltar")
            back.connect("clicked", self.come_back, data)
            grid.attach(back, 1, 9, 1, 1)
            if data['stage']>=3:
                self.set_data(data)
        else:
            button.set_label("Atualizar")
            button.connect("clicked", self.update, data[0])
            self.set_data(data, True)
        grid.attach(button, 2, 9, 1, 1)
    
    def simple_remove_letters(self, text):
        text = text.replace(",", "")
        text = text.replace(".", "")
        return text
    
    def next_step(self, widget, data):
        price = self.price.get_text().strip()
        price = price.replace(',', '.')
        if not self.simple_remove_letters(price).isnumeric():
            return UiDialog("Entrada inválida", "Por favor forneça um valor válido.")
        costPrice = self.costPrice.get_text().strip()
        costPrice = costPrice.replace(',', '.')
        if not self.simple_remove_letters(costPrice).isnumeric():
            return UiDialog("Entrada inválida", "Por favor forneça um valor válido.")
        
        stock = self.stock.get_text().strip()
        if not stock:
            stock = 0
        
        if data['stage']<3:
            data['stage'] = 3
        data['data']['price'] = price
        data['data']['costPrice'] = costPrice
        data['data']['stock'] = stock

        win = UiNextS4(data)
        win.show_all()
        return self.destroy()
    
    def update(self, widget, idProduct):
        price = self.price.get_text().strip()
        price = price.replace(',', '.')
        if not self.simple_remove_letters(price).isnumeric():
            return UiDialog("Entrada inválida!", "Por favor forneça um valor válido.")
        costPrice = self.costPrice.get_text().strip()
        costPrice = costPrice.replace(',', '.')
        if not self.simple_remove_letters(costPrice).isnumeric():
            return UiDialog("Entrada inválida!", "Por favor forneça um valor válido.")
        
        stock = self.stock.get_text().strip()
        if not stock:
            stock = 0
        
        submit = SbUpdateProduct()
        submit.set_product_id(idProduct)
        if not submit.update_price_stock([price, costPrice, stock]):
            return UiDialog("Erro ao enviar dados!", "Não foi possível enviar as informações para a base de dados.")
        return self.destroy()
    
    def come_back(self, widget, data):
        win = UiNextS2(data)
        win.show_all()
        return self.destroy()
    
    def set_data(self, data, other=False):
        if not other:
            self.price.set_text(data['data']['price'].replace(".", ","))
            self.costPrice.set_text(data['data']['costPrice'].replace(".", ","))
            self.stock.set_text(data['data']['stock'])
        else:
            self.price.set_text(str(data[1]).replace(".", ","))
            self.costPrice.set_text(str(data[2]).replace(".", ","))
            self.stock.set_text(str(data[3]))

class UiNextS4(Gtk.Window):

    def __init__(self, data=None, update=False):
        Gtk.Window.__init__(self, window_position="center")
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
        label = Gtk.Label(margin_bottom=20, halign="start")
        if not update:
            self.set_title("4ª Etapa - Novo produto")
            label.set_markup("<span size='21000'>Informações e Configurações</span>")
        else:
            self.set_title("Atualizar produto")
            label.set_markup("<span size='21000'>Atualizar informações e configurações</span>")
        grid.attach(label, 1, 1, 3, 1)

        # Tipo
        liststore = Gtk.ListStore(str)
        for item in ["Escolher", "Líquido", "Peso", "Tamanho"]:
            liststore.append([item])

        self.typeUnity = Gtk.ComboBox(width_request=150)
        self.typeUnity.set_model(liststore)
        self.typeUnity.set_active(0)
        self.typeUnity.connect("changed", self.on_event_01)

        cellrenderertext = Gtk.CellRendererText()
        self.typeUnity.pack_start(cellrenderertext, True)
        self.typeUnity.add_attribute(cellrenderertext, "text", 0)

        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Tipo de produto:</span><span color='red'>*</span>")
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.typeUnity, 1, 3, 1, 1)

        # Unidade
        self.unity = Gtk.ComboBoxText()
        listItems = [("0", "Escolher"), ("L", "Litros (L)"), ("Ml", "Mililitros (Ml)"),
         ("Kg", "Quilogramas (Kg)"), ("g", "Gramas (g)"),
          ("P", "Pequeno (P)"), ("M", "Médio (M)"), ("G", "Grande (G)")]
        for item in listItems:
            self.unity.append(item[0], item[1])
        self.unity.set_active_id("0")

        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Unidade:</span><span color='red'>*</span>")
        grid.attach(label, 1, 4, 1, 1)
        grid.attach(self.unity, 1, 5, 1, 1)

        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 1, 6, 1, 1)

        # Quantidade
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Peso/Volume:</span><span color='red'>*</span>")
        self.qUnity = Gtk.Entry()
        grid.attach(label, 1, 7, 1, 1)
        grid.attach(self.qUnity, 1, 8, 1, 1)

        # Pessoas servidas
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Pessoas servidas:</span>")
        self.people = Gtk.Entry(max_length=6)
        grid.attach(label, 1, 9, 1, 1)
        grid.attach(self.people, 1, 10, 1, 1)

        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL, margin_left=15, margin_right=15)
        grid.attach(separator, 2, 2, 1, 9)

        # Label info
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Configurações:</span>")
        grid.attach(label, 3, 2, 1, 1)

        # Cardápio virtual
        self.cvirtual = Gtk.CheckButton()
        self.cvirtual.set_label("Cardápio Virtual")
        self.cvirtual.set_active(True)
        grid.attach(self.cvirtual, 3, 3, 1, 1)

        # Delivery
        self.delivery = Gtk.CheckButton()
        self.delivery.set_label("Disponível para Delivery")
        self.delivery.set_active(False)
        grid.attach(self.delivery, 3, 4, 1, 1)

        # Pedido especial
        self.special = Gtk.CheckButton()
        self.special.set_label("Pedido Especial")
        self.special.set_active(False)
        grid.attach(self.special, 3, 5, 1, 1)

        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Pedido Especial:</span>\rautoriza ao cliente, solicitar\ra remoção de ingredientes.")
        grid.attach(label, 3, 6, 1, 2)
        
        # Seperator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(separator, 3, 8, 1, 1)

        # Categoria
        rData = SbCategory().get_categories()        
        self.category = Gtk.ComboBoxText(width_request=200)
        self.category.append("0", "Escolher")
        if rData['rStatus']==1:
            for item in rData['data']:
                self.category.append(str(item[0]), item[1])

        self.category.set_active_id("0")
        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Categoria:</span><span color='red'>*</span>")
        grid.attach(label, 3, 9, 1, 1)
        grid.attach(self.category, 3, 10, 1, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 11, 3, 1)

        label = Gtk.Label()
        label.set_markup("<span color='#c6262e' font='bold'>Depois desta estapa não é possível voltar. O produto será salvo.</span>")
        grid.attach(label, 1, 12, 3, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 13, 3, 1)

        button = Gtk.Button(height_request=40)
        if not update:
            button.set_label("Salvar")
            button.connect("clicked", self.next_step, data)
            back = Gtk.Button(height_request=40, label="Voltar")
            back.connect("clicked", self.come_back, data)
            grid.attach(back, 2, 14, 1, 1)
        else:
            button.set_label("Atualizar")
            button.connect("clicked", self.update, data[0])
            self.set_data(data)
        grid.attach(button, 3, 14, 1, 1)
    
    def next_step(self, widget, data):
        unity = self.unity.get_active_id()
        if unity == "0":
            return UiDialog("Entrada inválida", "Por favor preencha todos os campos.")
        amount = self.qUnity.get_text().strip()
        amount = amount.replace(",", ".")
        if not amount:
            amount = 0
        category = self.category.get_active_id()
        if category == "0":
            return UiDialog("Entrada inválida", "Por favor preencha todos os campos.")
        people = self.people.get_text().strip()
        if not people:
            people = 0
        cvirtual = self.cvirtual.get_active()
        delivery = self.delivery.get_active()
        special = self.special.get_active()
        self.destroy()
        # Enviar informações
        submit = SbNewProduct()
        result = submit.insert_meta_product([category, cvirtual, special, delivery, unity, amount, people])
        if result[0]:
            if not submit.insert_product([data['data']['code'], data['data']['name'], data['data']['description'], data['data']['ingre'], data['data']['price'], data['data']['costPrice'], data['data']['stock']]):
                submit.delete_meta_product()
                return UiDialog("Erro ao enviar dados", "Erro ao enviar dados. Por favor, tente novamente.")                
            win = UiDiscount([submit.get_product_id()])
            win.show_all()
        else:
            return UiDialog("Erro ao enviar dados", "Erro ao enviar dados. Por favor, tente novamente.")
    
    def update(self, widget, idProduct):
        unity = self.unity.get_active_id()
        if unity == "0":
            return UiDialog("Entrada inválida", "Por favor preencha todos os campos.")
        amount = self.qUnity.get_text().strip()
        amount = amount.replace(",", ".")
        if not amount:
            amount = 0
        category = self.category.get_active_id()
        if category == "0":
            return UiDialog("Entrada inválida", "Por favor preencha todos os campos.")
        people = self.people.get_text().strip()
        if not people:
            people = 0
        cvirtual = self.cvirtual.get_active()
        delivery = self.delivery.get_active()
        special = self.special.get_active()
        self.destroy()

        submit = SbUpdateProduct()
        submit.set_product_id(idProduct)
        if not submit.update_technical_information([category, cvirtual, special, delivery, unity, amount, people]):
            return UiDialog("Erro ao enviar dados!", "Não foi possível enviar as informações para a base de dados.")
        
    def come_back(self, widget, data):
        win = UiNextS3(data)
        win.show_all()
        return self.destroy()

    def on_event_01(self, widget):
        if widget.get_active() == 1:
            self.unity.remove_all()
            for item in [("0", "Escolher"), ("L", "Litros (L)"), ("Ml", "Mililitros (Ml)")]:
                self.unity.append(item[0], item[1])
            self.unity.set_active_id("L")
            self.qUnity.set_editable(True)            
        elif widget.get_active() == 2:
            self.unity.remove_all()            
            for item in [("0", "Escolher"), ("Kg", "Quilogramas (Kg)"), ("g", "Gramas (g)")]:
                self.unity.append(item[0], item[1])
            self.unity.set_active_id("Kg")
            self.qUnity.set_editable(True)            
        elif widget.get_active() == 3:
            self.unity.remove_all()            
            for item in [("0", "Escolher"), ("P", "Pequeno (P)"), ("M", "Médio (M)"), ("G", "Grande (G)")]:
                self.unity.append(item[0], item[1])
            self.unity.set_active_id("M")
            self.qUnity.set_text("0")
            self.qUnity.set_editable(False)
        else:
            self.unity.set_active(0)
    
    def set_data(self, data):
        self.unity.set_active_id(data[1])
        amount = str(data[2])
        if (amount[-2:]) == ".0":
            self.qUnity.set_text(amount[:-2])
        else:
            self.qUnity.set_text(amount)
        self.people.set_text(str(data[3]))
        self.cvirtual.set_active(bool(data[4]))
        self.delivery.set_active(bool(data[5]))
        self.special.set_active(bool(data[6]))
        self.category.set_active_id(str(data[7]))

class UiDiscount(Gtk.Window):

    def __init__(self, data=None, update=False):
        Gtk.Window.__init__(self, window_position="center")
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
        label = Gtk.Label(margin_bottom=20, halign="start")
        self.set_title("Descontos")
        label.set_markup("<span size='21000'>Descontos</span>")
        grid.attach(label, 1, 1, 2, 1)

        # Desconto por volume
        self.typeFree = Gtk.ComboBoxText()
        listItems = [("0", "Sem desconto"), ("percent", "Desconto por volume em porcentagem (%)"), ("money", "Desconto por volume em dinheiro (R$)"),
         ("unity", "Desconto por volume em volume (Unidades)")]
        for item in listItems:
            self.typeFree.append(item[0], item[1])
        self.typeFree.set_active_id("0")

        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Tipo de desconto:</span>")
        grid.attach(label, 1, 2, 1, 1)
        grid.attach(self.typeFree, 1, 3, 1, 1)

        button = Gtk.Button("Como funciona?")
        button.connect("clicked", self.on_popover_clicked)
        grid.attach(button, 1, 5, 1, 1)

        self.popover = Gtk.Popover()
        self.popover.set_position(Gtk.PositionType.RIGHT)
        self.popover.set_relative_to(button)

        box = Gtk.Box()
        box.set_spacing(5)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        self.popover.add(box)

        label = Gtk.Label(margin=10)
        label.set_markup("""<span color='#c6262e' font='bold'>Ex. (%):</span> a cada 4 unidades ou mais\ro cliente ganha 10% de desconto. 
<span color='#c6262e' font='bold'>Ex. (dinheiro):</span> a cada 4 unidades ou mais\ro cliente ganha 10 reais de desconto.
<span color='#c6262e' font='bold'>Ex. (unidade):</span> a cada 4 unidades ou mais\ro cliente ganha 1 unidade de desconto.""")
        box.add(label)

        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Valor do desconto:</span> <span color='#c6262e'>(somente números)</span>")
        self.value = Gtk.Entry(max_length=10)
        self.value.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.value.set_text("0")

        grid.attach(label, 2, 2, 1, 1)
        grid.attach(self.value, 2, 3, 1, 1)

        label = Gtk.Label(halign="start")
        label.set_markup("<span font='bold'>Quantidade do produto:</span>")
        self.quant = Gtk.Entry(max_length=10)
        self.quant.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.quant.set_text("0")

        grid.attach(label, 2, 4, 1, 1)
        grid.attach(self.quant, 2, 5, 1, 1)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, margin_top=10, margin_bottom=10)
        grid.attach(separator, 1, 9, 2, 1)

        button = Gtk.Button(height_request=40)
        button.set_label("Salvar")
        button.connect("clicked", self.submit, data[0])
        grid.attach(button, 1, 10, 1, 1)

        button = Gtk.Button(height_request=40)
        button.set_label("Fechar")
        button.connect("clicked", self.destroy_window)
        grid.attach(button, 2, 10, 2, 1)

        if update:
            self.set_data(data[1])
    
    def set_data(self, data):
        if data['free']!='0':
            self.typeFree.set_active_id(str(data['type']))
            self.value.set_text(str(data['free']).replace(".", ","))
            self.quant.set_text(str(data['quant']))
    
    def on_popover_clicked(self, button):
        self.popover.show_all()
    
    def simple_remove_letters(self, text):
        text = text.replace(",", "")
        text = text.replace(".", "")
        return text
    
    def submit(self, widget, idProduct):
        submit = SbUpdateProduct()
        submit.set_product_id(idProduct)

        # Envio sem desconto.
        typeFree = self.typeFree.get_active_id()
        if typeFree=="0":
            if not submit.update_discount({'free':'0'}):
                return UiDialog("Erro ao enviar dados!", "Não foi possível enviar as informações para a base de dados.")
            return self.destroy()
        else:
            # Envio com desconto.
            value = self.value.get_text().strip()
            value = value.replace(",", ".")
            if not self.simple_remove_letters(value).isnumeric():
                return UiDialog("Entrada inválida!", "Por favor, forneça um valor válido.")
            if value=='0':
                return UiDialog("Entrada inválida!", "Por favor, forneça um valor válido.")
            quant = self.quant.get_text().strip()
            if not quant.isnumeric():
                return UiDialog("Entrada inválida!", "Por favor, forneça um valor inteiro válido.")
            if quant=='0':
                return UiDialog("Entrada inválida!", "Por favor, forneça um valor válido.")
            if not submit.update_discount({'free':value, 'type':typeFree, 'quant':quant}):
                return UiDialog("Erro ao enviar dados!", "Não foi possível enviar as informações para a base de dados.")
            return self.destroy()
        
    def destroy_window(self, widget):
        return self.destroy()