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
from finalse_sdk.Amount import Amount
from finalse_sdk.FeesPayer import FeesPayer
from finalse_sdk.FeesValue import FeesValue
from typing import Dict
from typing import Optional
import json


class Fees:
    def __init__(self, payer: Optional[FeesPayer], value: FeesValue, amount: Amount):
        self._type = "Fees" 
        self.payer = payer
        self.value = value
        self.amount = amount

    @staticmethod
    def _type(): 
        return "Fees"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Fees.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('payer', self.payer.__to_remote_dict()),
            ('value', self.value.__to_remote_dict()),
            ('amount', self.amount.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('payer', self.payer.to_dict()),
            ('value', self.value.to_dict()),
            ('amount', self.amount.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Fees(FeesPayer.from_string(d["payer"]) if "payer" in d else None,
                    FeesValue.from_remote_dict(d["value"]),
                    Amount.from_remote_dict(d["amount"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Fees(FeesPayer.from_string(d["payer"]) if "payer" in d else None,
                    FeesValue.from_dict(d["value"]),
                    Amount.from_dict(d["amount"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Fees(payer=" + repr(self.payer) + 
                     ", value=" + repr(self.value) + 
                     ", amount=" + repr(self.amount) + ")")