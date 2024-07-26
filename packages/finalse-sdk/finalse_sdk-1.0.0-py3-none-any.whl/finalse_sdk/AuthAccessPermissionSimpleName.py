#   Copyright © 2024 Finalse Cloud
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from typing import Dict
import json


class AuthAccessPermissionSimpleName:
    def __init__(self, value: str):
        self._type = "AuthAccessPermissionSimpleName" 
        self.value = value

    @staticmethod
    def FullAccess():
        return AuthAccessPermissionSimpleName("FullAccess")

    @staticmethod
    def MoneyInOnly():
        return AuthAccessPermissionSimpleName("MoneyInOnly")

    @staticmethod
    def ReadMoneyIn():
        return AuthAccessPermissionSimpleName("ReadMoneyIn")

    @staticmethod
    def ReadOnly():
        return AuthAccessPermissionSimpleName("ReadOnly")

    @staticmethod
    def ReadWriteNoMoneyOut():
        return AuthAccessPermissionSimpleName("ReadWriteNoMoneyOut")

    @staticmethod
    def all_possibles_values():
        return {"FullAccess",
                "MoneyInOnly",
                "ReadMoneyIn",
                "ReadOnly",
                "ReadWriteNoMoneyOut"}

    @staticmethod
    def from_string(value):
        if value == "FullAccess": return AuthAccessPermissionSimpleName.FullAccess()
        elif value == "MoneyInOnly": return AuthAccessPermissionSimpleName.MoneyInOnly()
        elif value == "ReadMoneyIn": return AuthAccessPermissionSimpleName.ReadMoneyIn()
        elif value == "ReadOnly": return AuthAccessPermissionSimpleName.ReadOnly()
        elif value == "ReadWriteNoMoneyOut": return AuthAccessPermissionSimpleName.ReadWriteNoMoneyOut()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in AuthAccessPermissionSimpleName.all_possibles_values()

    def is_full_access(self):
        return self.value == "FullAccess"

    def is_money_in_only(self):
        return self.value == "MoneyInOnly"

    def is_read_money_in(self):
        return self.value == "ReadMoneyIn"

    def is_read_only(self):
        return self.value == "ReadOnly"

    def is_read_write_no_money_out(self):
        return self.value == "ReadWriteNoMoneyOut"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "AuthAccessPermissionSimpleName(value=" + self.value + ")"

    def __str__(self):
        return self.value