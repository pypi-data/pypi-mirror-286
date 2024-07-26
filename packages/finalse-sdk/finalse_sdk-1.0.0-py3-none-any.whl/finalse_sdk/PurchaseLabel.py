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


class PurchaseLabel:
    def __init__(self, value: str):
        self._type = "PurchaseLabel" 
        self.value = value

    @staticmethod
    def Buy():
        return PurchaseLabel("Buy")

    @staticmethod
    def Donate():
        return PurchaseLabel("Donate")

    @staticmethod
    def Participate():
        return PurchaseLabel("Participate")

    @staticmethod
    def Pay():
        return PurchaseLabel("Pay")

    @staticmethod
    def Subscribe():
        return PurchaseLabel("Subscribe")

    @staticmethod
    def all_possibles_values():
        return {"Buy",
                "Donate",
                "Participate",
                "Pay",
                "Subscribe"}

    @staticmethod
    def from_string(value):
        if value == "Buy": return PurchaseLabel.Buy()
        elif value == "Donate": return PurchaseLabel.Donate()
        elif value == "Participate": return PurchaseLabel.Participate()
        elif value == "Pay": return PurchaseLabel.Pay()
        elif value == "Subscribe": return PurchaseLabel.Subscribe()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in PurchaseLabel.all_possibles_values()

    def is_buy(self):
        return self.value == "Buy"

    def is_donate(self):
        return self.value == "Donate"

    def is_participate(self):
        return self.value == "Participate"

    def is_pay(self):
        return self.value == "Pay"

    def is_subscribe(self):
        return self.value == "Subscribe"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "PurchaseLabel(value=" + self.value + ")"

    def __str__(self):
        return self.value