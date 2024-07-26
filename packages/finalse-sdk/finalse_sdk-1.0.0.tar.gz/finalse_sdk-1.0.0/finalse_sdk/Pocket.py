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
from finalse_sdk.Balance import Balance
from finalse_sdk.Volume import Volume
from typing import Dict
import json


class Pocket:
    def __init__(self, balance: Balance, volume: Volume):
        self._type = "Pocket" 
        self.balance = balance
        self.volume = volume

    @staticmethod
    def _type(): 
        return "Pocket"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Pocket.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('balance', self.balance.__to_remote_dict()),
            ('volume', self.volume.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('balance', self.balance.to_dict()),
            ('volume', self.volume.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Pocket(Balance.from_remote_dict(d["balance"]),
                      Volume.from_remote_dict(d["volume"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Pocket(Balance.from_dict(d["balance"]),
                      Volume.from_dict(d["volume"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Pocket(balance=" + repr(self.balance) + 
                       ", volume=" + repr(self.volume) + ")")