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
from finalse_sdk.PurchaseLabel import PurchaseLabel
from typing import Dict
import json


class OtpAction(ABC):
    def is_login(self):
        return self._type == Login._type()

    def is_sign_up(self):
        return self._type == SignUp._type()

    def is_reset_secret(self):
        return self._type == ResetSecret._type()

    def isf_card_verify_notification_contact(self):
        return self._type == FCardVerifyNotificationContact._type()

    def isf_card_verify_validation_contact(self):
        return self._type == FCardVerifyValidationContact._type()

    def isf_card_view_balance(self):
        return self._type == FCardViewBalance._type()

    def isf_card_view_history(self):
        return self._type == FCardViewHistory._type()

    def isf_card_transfer(self):
        return self._type == FCardTransfer._type()

    def isf_card_quasi_transfer(self):
        return self._type == FCardQuasiTransfer._type()

    def is_receive_money(self):
        return self._type == ReceiveMoney._type()

    def is_money_move(self):
        return self._type == MoneyMove._type()

    def is_money_out(self):
        return self._type == MoneyOut._type()

    def is_purchase_formula(self):
        return self._type == PurchaseFormula._type()

    def as_login(self):
        if self.is_login():
            return self
        else:
            return None

    def as_sign_up(self):
        if self.is_sign_up():
            return self
        else:
            return None

    def as_reset_secret(self):
        if self.is_reset_secret():
            return self
        else:
            return None

    def as_f_card_verify_notification_contact(self):
        if self.is_f_card_verify_notification_contact():
            return self
        else:
            return None

    def as_f_card_verify_validation_contact(self):
        if self.is_f_card_verify_validation_contact():
            return self
        else:
            return None

    def as_f_card_view_balance(self):
        if self.is_f_card_view_balance():
            return self
        else:
            return None

    def as_f_card_view_history(self):
        if self.is_f_card_view_history():
            return self
        else:
            return None

    def as_f_card_transfer(self):
        if self.is_f_card_transfer():
            return self
        else:
            return None

    def as_f_card_quasi_transfer(self):
        if self.is_f_card_quasi_transfer():
            return self
        else:
            return None

    def as_receive_money(self):
        if self.is_receive_money():
            return self
        else:
            return None

    def as_money_move(self):
        if self.is_money_move():
            return self
        else:
            return None

    def as_money_out(self):
        if self.is_money_out():
            return self
        else:
            return None

    def as_purchase_formula(self):
        if self.is_purchase_formula():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return OtpAction.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Login._type(): return Login.from_remote_dict(d)
        elif ty == SignUp._type(): return SignUp.from_remote_dict(d);
        elif ty == ResetSecret._type(): return ResetSecret.from_remote_dict(d);
        elif ty == FCardVerifyNotificationContact._type(): return FCardVerifyNotificationContact.from_remote_dict(d);
        elif ty == FCardVerifyValidationContact._type(): return FCardVerifyValidationContact.from_remote_dict(d);
        elif ty == FCardViewBalance._type(): return FCardViewBalance.from_remote_dict(d);
        elif ty == FCardViewHistory._type(): return FCardViewHistory.from_remote_dict(d);
        elif ty == FCardTransfer._type(): return FCardTransfer.from_remote_dict(d);
        elif ty == FCardQuasiTransfer._type(): return FCardQuasiTransfer.from_remote_dict(d);
        elif ty == ReceiveMoney._type(): return ReceiveMoney.from_remote_dict(d);
        elif ty == MoneyMove._type(): return MoneyMove.from_remote_dict(d);
        elif ty == MoneyOut._type(): return MoneyOut.from_remote_dict(d);
        elif ty == PurchaseFormula._type(): return PurchaseFormula.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'OtpAction'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Login._type(): return Login.from_dict(d)
        elif ty == SignUp._type(): return SignUp.from_dict(d);
        elif ty == ResetSecret._type(): return ResetSecret.from_dict(d);
        elif ty == FCardVerifyNotificationContact._type(): return FCardVerifyNotificationContact.from_dict(d);
        elif ty == FCardVerifyValidationContact._type(): return FCardVerifyValidationContact.from_dict(d);
        elif ty == FCardViewBalance._type(): return FCardViewBalance.from_dict(d);
        elif ty == FCardViewHistory._type(): return FCardViewHistory.from_dict(d);
        elif ty == FCardTransfer._type(): return FCardTransfer.from_dict(d);
        elif ty == FCardQuasiTransfer._type(): return FCardQuasiTransfer.from_dict(d);
        elif ty == ReceiveMoney._type(): return ReceiveMoney.from_dict(d);
        elif ty == MoneyMove._type(): return MoneyMove.from_dict(d);
        elif ty == MoneyOut._type(): return MoneyOut.from_dict(d);
        elif ty == PurchaseFormula._type(): return PurchaseFormula.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'OtpAction'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class Login(OtpAction):
    def __init__(self):
        self._type = "Login" 
        super()

    @staticmethod
    def _type(): 
        return "Login"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Login.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Login()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Login()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Login"

class SignUp(OtpAction):
    def __init__(self):
        self._type = "SignUp" 
        super()

    @staticmethod
    def _type(): 
        return "SignUp"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return SignUp.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return SignUp()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return SignUp()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "SignUp"

class ResetSecret(OtpAction):
    def __init__(self):
        self._type = "ResetSecret" 
        super()

    @staticmethod
    def _type(): 
        return "ResetSecret"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return ResetSecret.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return ResetSecret()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return ResetSecret()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "ResetSecret"

class FCardVerifyNotificationContact(OtpAction):
    def __init__(self):
        self._type = "FCardVerifyNotificationContact" 
        super()

    @staticmethod
    def _type(): 
        return "FCardVerifyNotificationContact"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FCardVerifyNotificationContact.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FCardVerifyNotificationContact()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FCardVerifyNotificationContact()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FCardVerifyNotificationContact"

class FCardVerifyValidationContact(OtpAction):
    def __init__(self):
        self._type = "FCardVerifyValidationContact" 
        super()

    @staticmethod
    def _type(): 
        return "FCardVerifyValidationContact"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FCardVerifyValidationContact.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FCardVerifyValidationContact()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FCardVerifyValidationContact()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FCardVerifyValidationContact"

class FCardViewBalance(OtpAction):
    def __init__(self):
        self._type = "FCardViewBalance" 
        super()

    @staticmethod
    def _type(): 
        return "FCardViewBalance"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FCardViewBalance.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FCardViewBalance()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FCardViewBalance()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FCardViewBalance"

class FCardViewHistory(OtpAction):
    def __init__(self):
        self._type = "FCardViewHistory" 
        super()

    @staticmethod
    def _type(): 
        return "FCardViewHistory"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FCardViewHistory.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FCardViewHistory()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FCardViewHistory()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FCardViewHistory"

class FCardTransfer(OtpAction):
    def __init__(self):
        self._type = "FCardTransfer" 
        super()

    @staticmethod
    def _type(): 
        return "FCardTransfer"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FCardTransfer.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FCardTransfer()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FCardTransfer()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FCardTransfer"

class FCardQuasiTransfer(OtpAction):
    def __init__(self):
        self._type = "FCardQuasiTransfer" 
        super()

    @staticmethod
    def _type(): 
        return "FCardQuasiTransfer"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FCardQuasiTransfer.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FCardQuasiTransfer()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FCardQuasiTransfer()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "FCardQuasiTransfer"

class ReceiveMoney(OtpAction):
    def __init__(self, amount: Amount, sender_name: str):
        self._type = "ReceiveMoney" 
        super()
        self.amount = amount
        self.sender_name = sender_name

    @staticmethod
    def _type(): 
        return "ReceiveMoney"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return ReceiveMoney.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('amount', self.amount.__to_remote_dict()),
            ('senderName', self.sender_name)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('amount', self.amount.to_dict()),
            ('sender_name', self.sender_name)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return ReceiveMoney(Amount.from_remote_dict(d["amount"]),
                            d["senderName"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return ReceiveMoney(Amount.from_dict(d["amount"]),
                            d["sender_name"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("ReceiveMoney(amount=" + repr(self.amount) + 
                             ", sender_name=" + self.sender_name + ")")

class MoneyMove(OtpAction):
    def __init__(self, amount: Amount, receiver_name: str):
        self._type = "MoneyMove" 
        super()
        self.amount = amount
        self.receiver_name = receiver_name

    @staticmethod
    def _type(): 
        return "MoneyMove"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return MoneyMove.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('amount', self.amount.__to_remote_dict()),
            ('receiverName', self.receiver_name)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('amount', self.amount.to_dict()),
            ('receiver_name', self.receiver_name)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return MoneyMove(Amount.from_remote_dict(d["amount"]),
                         d["receiverName"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return MoneyMove(Amount.from_dict(d["amount"]),
                         d["receiver_name"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("MoneyMove(amount=" + repr(self.amount) + 
                          ", receiver_name=" + self.receiver_name + ")")

class MoneyOut(OtpAction):
    def __init__(self, amount: Amount, account: MoneyAccount):
        self._type = "MoneyOut" 
        super()
        self.amount = amount
        self.account = account

    @staticmethod
    def _type(): 
        return "MoneyOut"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return MoneyOut.from_remote_dict(value)

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
        return MoneyOut(Amount.from_remote_dict(d["amount"]),
                        MoneyAccount.from_remote_dict(d["account"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return MoneyOut(Amount.from_dict(d["amount"]),
                        MoneyAccount.from_dict(d["account"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("MoneyOut(amount=" + repr(self.amount) + 
                         ", account=" + repr(self.account) + ")")

class PurchaseFormula(OtpAction):
    def __init__(self, amount: Amount, merchant_name: str, purchase_label: PurchaseLabel):
        self._type = "PurchaseFormula" 
        super()
        self.amount = amount
        self.merchant_name = merchant_name
        self.purchase_label = purchase_label

    @staticmethod
    def _type(): 
        return "PurchaseFormula"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return PurchaseFormula.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('amount', self.amount.__to_remote_dict()),
            ('merchantName', self.merchant_name),
            ('purchaseLabel', str(self.purchase_label))
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('amount', self.amount.to_dict()),
            ('merchant_name', self.merchant_name),
            ('purchase_label', str(self.purchase_label))
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return PurchaseFormula(Amount.from_remote_dict(d["amount"]),
                               d["merchantName"],
                               PurchaseLabel.from_string(d["purchaseLabel"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return PurchaseFormula(Amount.from_dict(d["amount"]),
                               d["merchant_name"],
                               PurchaseLabel.from_string(d["purchase_label"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("PurchaseFormula(amount=" + repr(self.amount) + 
                                ", merchant_name=" + self.merchant_name + 
                                ", purchase_label=" + repr(self.purchase_label) + ")")