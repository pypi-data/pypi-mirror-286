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


class BalanceType:
    def __init__(self, value: str):
        self._type = "BalanceType" 
        self.value = value

    @staticmethod
    def AvailableBalance():
        return BalanceType("AvailableBalance")

    @staticmethod
    def LockedInBalance():
        return BalanceType("LockedInBalance")

    @staticmethod
    def LockedOutBalance():
        return BalanceType("LockedOutBalance")

    @staticmethod
    def all_possibles_values():
        return {"AvailableBalance",
                "LockedInBalance",
                "LockedOutBalance"}

    @staticmethod
    def from_string(value):
        if value == "AvailableBalance": return BalanceType.AvailableBalance()
        elif value == "LockedInBalance": return BalanceType.LockedInBalance()
        elif value == "LockedOutBalance": return BalanceType.LockedOutBalance()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in BalanceType.all_possibles_values()

    def is_available_balance(self):
        return self.value == "AvailableBalance"

    def is_locked_in_balance(self):
        return self.value == "LockedInBalance"

    def is_locked_out_balance(self):
        return self.value == "LockedOutBalance"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "BalanceType(value=" + self.value + ")"

    def __str__(self):
        return self.value