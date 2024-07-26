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


class AttemptParentType:
    def __init__(self, value: str):
        self._type = "AttemptParentType" 
        self.value = value

    @staticmethod
    def Deposit():
        return AttemptParentType("Deposit")

    @staticmethod
    def FormulaPurchase():
        return AttemptParentType("FormulaPurchase")

    @staticmethod
    def FundRequest():
        return AttemptParentType("FundRequest")

    @staticmethod
    def QuasiTransfer():
        return AttemptParentType("QuasiTransfer")

    @staticmethod
    def Refund():
        return AttemptParentType("Refund")

    @staticmethod
    def Transfer():
        return AttemptParentType("Transfer")

    @staticmethod
    def all_possibles_values():
        return {"Deposit",
                "FormulaPurchase",
                "FundRequest",
                "QuasiTransfer",
                "Refund",
                "Transfer"}

    @staticmethod
    def from_string(value):
        if value == "Deposit": return AttemptParentType.Deposit()
        elif value == "FormulaPurchase": return AttemptParentType.FormulaPurchase()
        elif value == "FundRequest": return AttemptParentType.FundRequest()
        elif value == "QuasiTransfer": return AttemptParentType.QuasiTransfer()
        elif value == "Refund": return AttemptParentType.Refund()
        elif value == "Transfer": return AttemptParentType.Transfer()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in AttemptParentType.all_possibles_values()

    def is_deposit(self):
        return self.value == "Deposit"

    def is_formula_purchase(self):
        return self.value == "FormulaPurchase"

    def is_fund_request(self):
        return self.value == "FundRequest"

    def is_quasi_transfer(self):
        return self.value == "QuasiTransfer"

    def is_refund(self):
        return self.value == "Refund"

    def is_transfer(self):
        return self.value == "Transfer"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "AttemptParentType(value=" + self.value + ")"

    def __str__(self):
        return self.value