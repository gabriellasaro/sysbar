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
class SbDateFormat():

    def __init__(self, date):
        self.date = date
    
    def diff_passed_to_current(self):
        diff = int((datetime.now()-datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S')).total_seconds()/60)
        if diff>=60:
            hours = int(diff/60)
            if hours>24:
                day = int(hours/24)
                if day>11:
                    return self.date
                return "{} dias atrás".format(day)
            return "{} hora(s) atrás".format(hours)
        elif diff<=0:
            return "<1 minuto atrás"
        else:
            return "{} minutos atrás".format(diff)