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
from datetime import datetime
class ValidateInput():

    def validate_pin(self, pin):
        if len(pin)>4 or len(pin)<4:
            return False
        else:
            if not pin.isdigit():
                return False
            else:
                return True
    def validate_phone(self, phone):
        if len(phone)<11 or len(phone)>12:
            return False
        else:
            if not phone.isdigit():
                return False
            else:
                return True
    
    def validate_name(self, name):
        if len(name)>120 or len(name)==0:
            return False
        else:
            return True
    
    def validate_date(self, date):
        if date == None:
            return False
        elif len(date)<8 or len(date)>10:
            return False
        else:
            return True
    
    # Remover função format_date no futuro
    def format_date(self, date):
        date = date.replace("-", "")
        date = date.replace("/", "")
        date = date.replace(".", "")
        result = datetime.strptime(date, '%d%m%Y')
        return result.strftime('%Y-%m-%d')

class SbFormatString():

    def get_months(self):
        months = {
            '01':'Janeiro',
            '02':'Fevereiro',
            '03':'Março',
            '04':'Abril',
            '05':'Maio',
            '06':'Junho',
            '07':'Julho',
            '08':'Agosto',
            '09':'Setembro',
            '10':'Outubro',
            '11':'Novembro',
            '12':'Dezembro'
        }
        return months

    def format_string_for_date(self, date):
        date = date.replace("-", "")
        date = date.replace("/", "")
        date = date.replace(".", "")
        result = datetime.strptime(date, '%d%m%Y')
        return result.strftime('%Y-%m-%d')
    
    def format_date_for_string(self, date):
        date = date.split('-')
        return "{} de {} de {}".format(date[2], self.get_months()[date[1]], date[0])