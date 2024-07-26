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
from typing import Dict
from typing import Optional
import json


class TransactionDetails(ABC):
    def is_mobile_money_transfer(self):
        return self._type == MobileMoneyTransfer._type()

    def isf_pay_transfer(self):
        return self._type == FPayTransfer._type()

    def is_bank_transfer(self):
        return self._type == BankTransfer._type()

    def as_mobile_money_transfer(self):
        if self.is_mobile_money_transfer():
            return self
        else:
            return None

    def as_f_pay_transfer(self):
        if self.is_f_pay_transfer():
            return self
        else:
            return None

    def as_bank_transfer(self):
        if self.is_bank_transfer():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return TransactionDetails.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == MobileMoneyTransfer._type(): return MobileMoneyTransfer.from_remote_dict(d)
        elif ty == FPayTransfer._type(): return FPayTransfer.from_remote_dict(d);
        elif ty == BankTransfer._type(): return BankTransfer.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransactionDetails'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == MobileMoneyTransfer._type(): return MobileMoneyTransfer.from_dict(d)
        elif ty == FPayTransfer._type(): return FPayTransfer.from_dict(d);
        elif ty == BankTransfer._type(): return BankTransfer.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransactionDetails'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class MobileMoneyTransfer(TransactionDetails):
    def __init__(self, provider_transaction_id: Optional[str]):
        self._type = "MobileMoneyTransfer" 
        super()
        self.provider_transaction_id = provider_transaction_id

    @staticmethod
    def _type(): 
        return "MobileMoneyTransfer"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return MobileMoneyTransfer.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('providerTransactionId', self.provider_transaction_id)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('provider_transaction_id', self.provider_transaction_id)])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return MobileMoneyTransfer(d["providerTransactionId"] if "providerTransactionId" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return MobileMoneyTransfer(d["provider_transaction_id"] if "provider_transaction_id" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "MobileMoneyTransfer(provider_transaction_id=" + str(self.provider_transaction_id) + ")"

class FPayTransfer(TransactionDetails):
    def __init__(self):
        self._type = "FPayTransfer" 
        super()

    @staticmethod
    def _type(): 
        return "FPayTransfer"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FPayTransfer.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FPayTransfer()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FPayTransfer()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FPayTransfer"

class BankTransfer(TransactionDetails):
    def __init__(self):
        self._type = "BankTransfer" 
        super()

    @staticmethod
    def _type(): 
        return "BankTransfer"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return BankTransfer.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return BankTransfer()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return BankTransfer()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "BankTransfer"