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
from abc import ABC, abstractmethod
from finalse_sdk.Amount import Amount
from finalse_sdk.MoneyAccount import MoneyAccount
from typing import Dict
import json


class Source(ABC):
    def is_single(self):
        return self._type == Single._type()

    def is_multiple(self):
        return self._type == Multiple._type()

    def as_single(self):
        if self.is_single():
            return self
        else:
            return None

    def as_multiple(self):
        if self.is_multiple():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Source.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Single._type(): return Single.from_remote_dict(d)
        elif ty == Multiple._type(): return Multiple.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'Source'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Single._type(): return Single.from_dict(d)
        elif ty == Multiple._type(): return Multiple.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'Source'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class Single(Source):
    def __init__(self, amount: Amount, account: MoneyAccount):
        self._type = "Single" 
        super()
        self.amount = amount
        self.account = account

    @staticmethod
    def _type(): 
        return "Single"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Single.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('amount', self.amount.__to_remote_dict()),
            ('account', self.account.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('amount', self.amount.to_dict()),
            ('account', self.account.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Single(Amount.from_remote_dict(d["amount"]),
                      MoneyAccount.from_remote_dict(d["account"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Single(Amount.from_dict(d["amount"]),
                      MoneyAccount.from_dict(d["account"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Single(amount=" + repr(self.amount) + 
                       ", account=" + repr(self.account) + ")")

class Multiple(Source):
    def __init__(self):
        self._type = "Multiple" 
        super()

    @staticmethod
    def _type(): 
        return "Multiple"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Multiple.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Multiple()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Multiple()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Multiple"