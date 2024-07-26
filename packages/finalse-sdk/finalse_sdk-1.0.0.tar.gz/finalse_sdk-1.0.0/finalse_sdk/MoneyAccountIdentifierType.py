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


class MoneyAccountIdentifierType:
    def __init__(self, value: str):
        self._type = "MoneyAccountIdentifierType" 
        self.value = value

    @staticmethod
    def Iban():
        return MoneyAccountIdentifierType("Iban")

    @staticmethod
    def Id():
        return MoneyAccountIdentifierType("Id")

    @staticmethod
    def Man():
        return MoneyAccountIdentifierType("Man")

    @staticmethod
    def MobileNumber():
        return MoneyAccountIdentifierType("MobileNumber")

    @staticmethod
    def all_possibles_values():
        return {"Iban",
                "Id",
                "Man",
                "MobileNumber"}

    @staticmethod
    def from_string(value):
        if value == "Iban": return MoneyAccountIdentifierType.Iban()
        elif value == "Id": return MoneyAccountIdentifierType.Id()
        elif value == "Man": return MoneyAccountIdentifierType.Man()
        elif value == "MobileNumber": return MoneyAccountIdentifierType.MobileNumber()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in MoneyAccountIdentifierType.all_possibles_values()

    def is_iban(self):
        return self.value == "Iban"

    def is_id(self):
        return self.value == "Id"

    def is_man(self):
        return self.value == "Man"

    def is_mobile_number(self):
        return self.value == "MobileNumber"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "MoneyAccountIdentifierType(value=" + self.value + ")"

    def __str__(self):
        return self.value