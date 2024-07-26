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
from finalse_sdk.AmountCurrency import AmountCurrency
from typing import Dict
import json


class Amount:
    def __init__(self, value: float, currency: AmountCurrency):
        self._type = "Amount" 
        self.value = value
        self.currency = currency

    @staticmethod
    def _type(): 
        return "Amount"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Amount.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('value', self.value),
            ('currency', self.currency.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('value', self.value),
            ('currency', self.currency.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Amount(d["value"],
                      AmountCurrency.from_remote_dict(d["currency"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Amount(d["value"],
                      AmountCurrency.from_dict(d["currency"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Amount(value=" + str(self.value) + 
                       ", currency=" + repr(self.currency) + ")")