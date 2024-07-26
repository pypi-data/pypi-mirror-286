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
from finalse_sdk.BalanceType import BalanceType
from finalse_sdk.MoneyAccountIdentifier import MoneyAccountIdentifier
from finalse_sdk.MoneyAccountProvider import MoneyAccountProvider
from typing import Dict
import json


class MoneyAccount:
    def __init__(self,
                 balance_type: BalanceType,
                 provider: MoneyAccountProvider,
                 identifier: MoneyAccountIdentifier):
        self._type = "MoneyAccount" 
        self.balance_type = balance_type
        self.provider = provider
        self.identifier = identifier

    @staticmethod
    def _type(): 
        return "MoneyAccount"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return MoneyAccount.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('balanceType', str(self.balance_type)),
            ('provider', self.provider.__to_remote_dict()),
            ('identifier', self.identifier.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('balance_type', str(self.balance_type)),
            ('provider', self.provider.to_dict()),
            ('identifier', self.identifier.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return MoneyAccount(BalanceType.from_string(d["balanceType"]),
                            MoneyAccountProvider.from_remote_dict(d["provider"]),
                            MoneyAccountIdentifier.from_remote_dict(d["identifier"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return MoneyAccount(BalanceType.from_string(d["balance_type"]),
                            MoneyAccountProvider.from_dict(d["provider"]),
                            MoneyAccountIdentifier.from_dict(d["identifier"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("MoneyAccount(balance_type=" + repr(self.balance_type) + 
                             ", provider=" + repr(self.provider) + 
                             ", identifier=" + repr(self.identifier) + ")")