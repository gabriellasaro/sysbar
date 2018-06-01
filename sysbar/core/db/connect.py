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
import sqlite3
class DBSysbar():

    def conn(self, cursor = False):
        conn = sqlite3.connect('/home/gabriel/.system-bar/database/sysbar.db')
        if cursor:
            return conn.cursor()
        return conn

class DBUsers():

    def conn(self, cursor = False):
        conn = sqlite3.connect('/home/gabriel/.system-bar/database/users.db')
        if cursor:
            return conn.cursor()
        return conn