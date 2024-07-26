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
from finalse_sdk.AuthAccessPermission import AuthAccessPermission
from finalse_sdk.Creator import Creator
from finalse_sdk.DepositStatus import DepositStatus
from finalse_sdk.Destination import Destination
from finalse_sdk.Expire import Expire
from finalse_sdk.Fees import Fees
from finalse_sdk.FundRequestStatus import FundRequestStatus
from finalse_sdk.H1Descriptor import H1Descriptor
from finalse_sdk.LightAttempt import LightAttempt
from finalse_sdk.Man import Man
from finalse_sdk.Mars import Mars
from finalse_sdk.OnFundRequestCompleted import OnFundRequestCompleted
from finalse_sdk.OnQuasiTransferCompleted import OnQuasiTransferCompleted
from finalse_sdk.Pocket import Pocket
from finalse_sdk.QuasiTransferStatus import QuasiTransferStatus
from finalse_sdk.SecurePay import SecurePay
from finalse_sdk.Sending import Sending
from finalse_sdk.Source import Source
from finalse_sdk.TransferStatus import TransferStatus
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
from typing import Optional
import json


class TransactionParent(ABC):
    def is_refund(self):
        return self._type == Refund._type()

    def is_auth_access(self):
        return self._type == AuthAccess._type()

    def is_deposit(self):
        return self._type == Deposit._type()

    def is_formula_purchase(self):
        return self._type == FormulaPurchase._type()

    def is_fund_request(self):
        return self._type == FundRequest._type()

    def is_quasi_transfer(self):
        return self._type == QuasiTransfer._type()

    def is_transfer(self):
        return self._type == Transfer._type()

    def is_wallet(self):
        return self._type == Wallet._type()

    def as_refund(self):
        if self.is_refund():
            return self
        else:
            return None

    def as_auth_access(self):
        if self.is_auth_access():
            return self
        else:
            return None

    def as_deposit(self):
        if self.is_deposit():
            return self
        else:
            return None

    def as_formula_purchase(self):
        if self.is_formula_purchase():
            return self
        else:
            return None

    def as_fund_request(self):
        if self.is_fund_request():
            return self
        else:
            return None

    def as_quasi_transfer(self):
        if self.is_quasi_transfer():
            return self
        else:
            return None

    def as_transfer(self):
        if self.is_transfer():
            return self
        else:
            return None

    def as_wallet(self):
        if self.is_wallet():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return TransactionParent.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Refund._type(): return Refund.from_remote_dict(d)
        elif ty == AuthAccess._type(): return AuthAccess.from_remote_dict(d);
        elif ty == Deposit._type(): return Deposit.from_remote_dict(d);
        elif ty == FormulaPurchase._type(): return FormulaPurchase.from_remote_dict(d);
        elif ty == FundRequest._type(): return FundRequest.from_remote_dict(d);
        elif ty == QuasiTransfer._type(): return QuasiTransfer.from_remote_dict(d);
        elif ty == Transfer._type(): return Transfer.from_remote_dict(d);
        elif ty == Wallet._type(): return Wallet.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransactionParent'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Refund._type(): return Refund.from_dict(d)
        elif ty == AuthAccess._type(): return AuthAccess.from_dict(d);
        elif ty == Deposit._type(): return Deposit.from_dict(d);
        elif ty == FormulaPurchase._type(): return FormulaPurchase.from_dict(d);
        elif ty == FundRequest._type(): return FundRequest.from_dict(d);
        elif ty == QuasiTransfer._type(): return QuasiTransfer.from_dict(d);
        elif ty == Transfer._type(): return Transfer.from_dict(d);
        elif ty == Wallet._type(): return Wallet.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransactionParent'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class Refund(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str]):
        self._type = "Refund" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data

    @staticmethod
    def _type(): 
        return "Refund"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Refund.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Refund(d["id"],
                      d["url"],
                      d["description"] if "description" in d else None,
                      Creator.from_remote_dict(d["creator"]),
                      d["foreignId"] if "foreignId" in d else None,
                      d["foreignData"] if "foreignData" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Refund(d["id"],
                      d["url"],
                      d["description"] if "description" in d else None,
                      Creator.from_dict(d["creator"]),
                      d["foreign_id"] if "foreign_id" in d else None,
                      d["foreign_data"] if "foreign_data" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Refund(id=" + self.id + 
                       ", url=" + self.url + 
                       ", description=" + str(self.description) + 
                       ", creator=" + repr(self.creator) + 
                       ", foreign_id=" + str(self.foreign_id) + 
                       ", foreign_data=" + str(self.foreign_data) + ")")

class AuthAccess(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str],
                 created_time: UTCDateTime,
                 name: str,
                 token: str,
                 permission: AuthAccessPermission,
                 secret_key: str,
                 is_enabled: bool):
        self._type = "AuthAccess" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data
        self.created_time = created_time
        self.name = name
        self.token = token
        self.permission = permission
        self.secret_key = secret_key
        self.is_enabled = is_enabled

    @staticmethod
    def _type(): 
        return "AuthAccess"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return AuthAccess.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('name', self.name),
            ('token', self.token),
            ('permission', self.permission.__to_remote_dict()),
            ('secretKey', self.secret_key),
            ('isEnabled', self.is_enabled)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data),
            ('created_time', self.created_time.to_dict()),
            ('name', self.name),
            ('token', self.token),
            ('permission', self.permission.to_dict()),
            ('secret_key', self.secret_key),
            ('is_enabled', self.is_enabled)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return AuthAccess(d["id"],
                          d["url"],
                          d["description"] if "description" in d else None,
                          Creator.from_remote_dict(d["creator"]),
                          d["foreignId"] if "foreignId" in d else None,
                          d["foreignData"] if "foreignData" in d else None,
                          UTCDateTime.from_remote_dict(d["createdTime"]),
                          d["name"],
                          d["token"],
                          AuthAccessPermission.from_remote_dict(d["permission"]),
                          d["secretKey"],
                          d["isEnabled"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return AuthAccess(d["id"],
                          d["url"],
                          d["description"] if "description" in d else None,
                          Creator.from_dict(d["creator"]),
                          d["foreign_id"] if "foreign_id" in d else None,
                          d["foreign_data"] if "foreign_data" in d else None,
                          UTCDateTime.from_dict(d["created_time"]),
                          d["name"],
                          d["token"],
                          AuthAccessPermission.from_dict(d["permission"]),
                          d["secret_key"],
                          d["is_enabled"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("AuthAccess(id=" + self.id + 
                           ", url=" + self.url + 
                           ", description=" + str(self.description) + 
                           ", creator=" + repr(self.creator) + 
                           ", foreign_id=" + str(self.foreign_id) + 
                           ", foreign_data=" + str(self.foreign_data) + 
                           ", created_time=" + repr(self.created_time) + 
                           ", name=" + self.name + 
                           ", token=" + self.token + 
                           ", permission=" + repr(self.permission) + 
                           ", secret_key=******" + 
                           ", is_enabled=" + str(self.is_enabled) + ")")

class Deposit(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str],
                 created_time: UTCDateTime,
                 completed_time: Optional[UTCDateTime],
                 h1_descriptor: Optional[H1Descriptor],
                 source: Source,
                 destination: Destination,
                 fees: Fees,
                 attempt: LightAttempt,
                 amount: Amount,
                 sending: Sending,
                 status: DepositStatus):
        self._type = "Deposit" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data
        self.created_time = created_time
        self.completed_time = completed_time
        self.h1_descriptor = h1_descriptor
        self.source = source
        self.destination = destination
        self.fees = fees
        self.attempt = attempt
        self.amount = amount
        self.sending = sending
        self.status = status

    @staticmethod
    def _type(): 
        return "Deposit"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Deposit.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('completedTime', self.completed_time.__to_remote_dict()),
            ('h1Descriptor', self.h1_descriptor.__to_remote_dict()),
            ('source', self.source.__to_remote_dict()),
            ('destination', self.destination.__to_remote_dict()),
            ('fees', self.fees.__to_remote_dict()),
            ('attempt', self.attempt.__to_remote_dict()),
            ('amount', self.amount.__to_remote_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data),
            ('created_time', self.created_time.to_dict()),
            ('completed_time', self.completed_time.to_dict()),
            ('h1_descriptor', self.h1_descriptor.to_dict()),
            ('source', self.source.to_dict()),
            ('destination', self.destination.to_dict()),
            ('fees', self.fees.to_dict()),
            ('attempt', self.attempt.to_dict()),
            ('amount', self.amount.to_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Deposit(d["id"],
                       d["url"],
                       d["description"] if "description" in d else None,
                       Creator.from_remote_dict(d["creator"]),
                       d["foreignId"] if "foreignId" in d else None,
                       d["foreignData"] if "foreignData" in d else None,
                       UTCDateTime.from_remote_dict(d["createdTime"]),
                       UTCDateTime.from_remote_dict(d["completedTime"]) if "completedTime" in d else None,
                       H1Descriptor.from_remote_dict(d["h1Descriptor"]) if "h1Descriptor" in d else None,
                       Source.from_remote_dict(d["source"]),
                       Destination.from_remote_dict(d["destination"]),
                       Fees.from_remote_dict(d["fees"]),
                       LightAttempt.from_remote_dict(d["attempt"]),
                       Amount.from_remote_dict(d["amount"]),
                       Sending.from_string(d["sending"]),
                       DepositStatus.from_remote_dict(d["status"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Deposit(d["id"],
                       d["url"],
                       d["description"] if "description" in d else None,
                       Creator.from_dict(d["creator"]),
                       d["foreign_id"] if "foreign_id" in d else None,
                       d["foreign_data"] if "foreign_data" in d else None,
                       UTCDateTime.from_dict(d["created_time"]),
                       UTCDateTime.from_dict(d["completed_time"]) if "completed_time" in d else None,
                       H1Descriptor.from_dict(d["h1_descriptor"]) if "h1_descriptor" in d else None,
                       Source.from_dict(d["source"]),
                       Destination.from_dict(d["destination"]),
                       Fees.from_dict(d["fees"]),
                       LightAttempt.from_dict(d["attempt"]),
                       Amount.from_dict(d["amount"]),
                       Sending.from_string(d["sending"]),
                       DepositStatus.from_dict(d["status"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Deposit(id=" + self.id + 
                        ", url=" + self.url + 
                        ", description=" + str(self.description) + 
                        ", creator=" + repr(self.creator) + 
                        ", foreign_id=" + str(self.foreign_id) + 
                        ", foreign_data=" + str(self.foreign_data) + 
                        ", created_time=" + repr(self.created_time) + 
                        ", completed_time=" + repr(self.completed_time) + 
                        ", h1_descriptor=" + repr(self.h1_descriptor) + 
                        ", source=" + repr(self.source) + 
                        ", destination=" + repr(self.destination) + 
                        ", fees=" + repr(self.fees) + 
                        ", attempt=" + repr(self.attempt) + 
                        ", amount=" + repr(self.amount) + 
                        ", sending=" + repr(self.sending) + 
                        ", status=" + repr(self.status) + ")")

class FormulaPurchase(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str]):
        self._type = "FormulaPurchase" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data

    @staticmethod
    def _type(): 
        return "FormulaPurchase"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FormulaPurchase.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FormulaPurchase(d["id"],
                               d["url"],
                               d["description"] if "description" in d else None,
                               Creator.from_remote_dict(d["creator"]),
                               d["foreignId"] if "foreignId" in d else None,
                               d["foreignData"] if "foreignData" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FormulaPurchase(d["id"],
                               d["url"],
                               d["description"] if "description" in d else None,
                               Creator.from_dict(d["creator"]),
                               d["foreign_id"] if "foreign_id" in d else None,
                               d["foreign_data"] if "foreign_data" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("FormulaPurchase(id=" + self.id + 
                                ", url=" + self.url + 
                                ", description=" + str(self.description) + 
                                ", creator=" + repr(self.creator) + 
                                ", foreign_id=" + str(self.foreign_id) + 
                                ", foreign_data=" + str(self.foreign_data) + ")")

class FundRequest(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str],
                 created_time: UTCDateTime,
                 completed_time: Optional[UTCDateTime],
                 h1_descriptor: Optional[H1Descriptor],
                 secure_pay: SecurePay,
                 amount: Optional[Amount],
                 sending: Sending,
                 status: FundRequestStatus,
                 source: Optional[Source],
                 destination: Destination,
                 fees: Fees,
                 expire: Optional[Expire],
                 on_success: Optional[OnFundRequestCompleted],
                 on_failure: Optional[OnFundRequestCompleted]):
        self._type = "FundRequest" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data
        self.created_time = created_time
        self.completed_time = completed_time
        self.h1_descriptor = h1_descriptor
        self.secure_pay = secure_pay
        self.amount = amount
        self.sending = sending
        self.status = status
        self.source = source
        self.destination = destination
        self.fees = fees
        self.expire = expire
        self.on_success = on_success
        self.on_failure = on_failure

    @staticmethod
    def _type(): 
        return "FundRequest"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return FundRequest.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('completedTime', self.completed_time.__to_remote_dict()),
            ('h1Descriptor', self.h1_descriptor.__to_remote_dict()),
            ('securePay', self.secure_pay.__to_remote_dict()),
            ('amount', self.amount.__to_remote_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.__to_remote_dict()),
            ('source', self.source.__to_remote_dict()),
            ('destination', self.destination.__to_remote_dict()),
            ('fees', self.fees.__to_remote_dict()),
            ('expire', self.expire.__to_remote_dict()),
            ('onSuccess', self.on_success.__to_remote_dict()),
            ('onFailure', self.on_failure.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data),
            ('created_time', self.created_time.to_dict()),
            ('completed_time', self.completed_time.to_dict()),
            ('h1_descriptor', self.h1_descriptor.to_dict()),
            ('secure_pay', self.secure_pay.to_dict()),
            ('amount', self.amount.to_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.to_dict()),
            ('source', self.source.to_dict()),
            ('destination', self.destination.to_dict()),
            ('fees', self.fees.to_dict()),
            ('expire', self.expire.to_dict()),
            ('on_success', self.on_success.to_dict()),
            ('on_failure', self.on_failure.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return FundRequest(d["id"],
                           d["url"],
                           d["description"] if "description" in d else None,
                           Creator.from_remote_dict(d["creator"]),
                           d["foreignId"] if "foreignId" in d else None,
                           d["foreignData"] if "foreignData" in d else None,
                           UTCDateTime.from_remote_dict(d["createdTime"]),
                           UTCDateTime.from_remote_dict(d["completedTime"]) if "completedTime" in d else None,
                           H1Descriptor.from_remote_dict(d["h1Descriptor"]) if "h1Descriptor" in d else None,
                           SecurePay.from_remote_dict(d["securePay"]),
                           Amount.from_remote_dict(d["amount"]) if "amount" in d else None,
                           Sending.from_string(d["sending"]),
                           FundRequestStatus.from_remote_dict(d["status"]),
                           Source.from_remote_dict(d["source"]) if "source" in d else None,
                           Destination.from_remote_dict(d["destination"]),
                           Fees.from_remote_dict(d["fees"]),
                           Expire.from_remote_dict(d["expire"]) if "expire" in d else None,
                           OnFundRequestCompleted.from_remote_dict(d["onSuccess"]) if "onSuccess" in d else None,
                           OnFundRequestCompleted.from_remote_dict(d["onFailure"]) if "onFailure" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return FundRequest(d["id"],
                           d["url"],
                           d["description"] if "description" in d else None,
                           Creator.from_dict(d["creator"]),
                           d["foreign_id"] if "foreign_id" in d else None,
                           d["foreign_data"] if "foreign_data" in d else None,
                           UTCDateTime.from_dict(d["created_time"]),
                           UTCDateTime.from_dict(d["completed_time"]) if "completed_time" in d else None,
                           H1Descriptor.from_dict(d["h1_descriptor"]) if "h1_descriptor" in d else None,
                           SecurePay.from_dict(d["secure_pay"]),
                           Amount.from_dict(d["amount"]) if "amount" in d else None,
                           Sending.from_string(d["sending"]),
                           FundRequestStatus.from_dict(d["status"]),
                           Source.from_dict(d["source"]) if "source" in d else None,
                           Destination.from_dict(d["destination"]),
                           Fees.from_dict(d["fees"]),
                           Expire.from_dict(d["expire"]) if "expire" in d else None,
                           OnFundRequestCompleted.from_dict(d["on_success"]) if "on_success" in d else None,
                           OnFundRequestCompleted.from_dict(d["on_failure"]) if "on_failure" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("FundRequest(id=" + self.id + 
                            ", url=" + self.url + 
                            ", description=" + str(self.description) + 
                            ", creator=" + repr(self.creator) + 
                            ", foreign_id=" + str(self.foreign_id) + 
                            ", foreign_data=" + str(self.foreign_data) + 
                            ", created_time=" + repr(self.created_time) + 
                            ", completed_time=" + repr(self.completed_time) + 
                            ", h1_descriptor=" + repr(self.h1_descriptor) + 
                            ", secure_pay=" + repr(self.secure_pay) + 
                            ", amount=" + repr(self.amount) + 
                            ", sending=" + repr(self.sending) + 
                            ", status=" + repr(self.status) + 
                            ", source=" + repr(self.source) + 
                            ", destination=" + repr(self.destination) + 
                            ", fees=" + repr(self.fees) + 
                            ", expire=" + repr(self.expire) + 
                            ", on_success=" + repr(self.on_success) + 
                            ", on_failure=" + repr(self.on_failure) + ")")

class QuasiTransfer(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str],
                 created_time: UTCDateTime,
                 completed_time: Optional[UTCDateTime],
                 h1_descriptor: Optional[H1Descriptor],
                 secure_pay: SecurePay,
                 amount: Optional[Amount],
                 sending: Sending,
                 status: QuasiTransferStatus,
                 source: Source,
                 destination: Optional[Destination],
                 fees: Fees,
                 expire: Optional[Expire],
                 on_success: Optional[OnQuasiTransferCompleted],
                 on_failure: Optional[OnQuasiTransferCompleted]):
        self._type = "QuasiTransfer" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data
        self.created_time = created_time
        self.completed_time = completed_time
        self.h1_descriptor = h1_descriptor
        self.secure_pay = secure_pay
        self.amount = amount
        self.sending = sending
        self.status = status
        self.source = source
        self.destination = destination
        self.fees = fees
        self.expire = expire
        self.on_success = on_success
        self.on_failure = on_failure

    @staticmethod
    def _type(): 
        return "QuasiTransfer"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return QuasiTransfer.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('completedTime', self.completed_time.__to_remote_dict()),
            ('h1Descriptor', self.h1_descriptor.__to_remote_dict()),
            ('securePay', self.secure_pay.__to_remote_dict()),
            ('amount', self.amount.__to_remote_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.__to_remote_dict()),
            ('source', self.source.__to_remote_dict()),
            ('destination', self.destination.__to_remote_dict()),
            ('fees', self.fees.__to_remote_dict()),
            ('expire', self.expire.__to_remote_dict()),
            ('onSuccess', self.on_success.__to_remote_dict()),
            ('onFailure', self.on_failure.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data),
            ('created_time', self.created_time.to_dict()),
            ('completed_time', self.completed_time.to_dict()),
            ('h1_descriptor', self.h1_descriptor.to_dict()),
            ('secure_pay', self.secure_pay.to_dict()),
            ('amount', self.amount.to_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.to_dict()),
            ('source', self.source.to_dict()),
            ('destination', self.destination.to_dict()),
            ('fees', self.fees.to_dict()),
            ('expire', self.expire.to_dict()),
            ('on_success', self.on_success.to_dict()),
            ('on_failure', self.on_failure.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return QuasiTransfer(d["id"],
                             d["url"],
                             d["description"] if "description" in d else None,
                             Creator.from_remote_dict(d["creator"]),
                             d["foreignId"] if "foreignId" in d else None,
                             d["foreignData"] if "foreignData" in d else None,
                             UTCDateTime.from_remote_dict(d["createdTime"]),
                             UTCDateTime.from_remote_dict(d["completedTime"]) if "completedTime" in d else None,
                             H1Descriptor.from_remote_dict(d["h1Descriptor"]) if "h1Descriptor" in d else None,
                             SecurePay.from_remote_dict(d["securePay"]),
                             Amount.from_remote_dict(d["amount"]) if "amount" in d else None,
                             Sending.from_string(d["sending"]),
                             QuasiTransferStatus.from_remote_dict(d["status"]),
                             Source.from_remote_dict(d["source"]),
                             Destination.from_remote_dict(d["destination"]) if "destination" in d else None,
                             Fees.from_remote_dict(d["fees"]),
                             Expire.from_remote_dict(d["expire"]) if "expire" in d else None,
                             OnQuasiTransferCompleted.from_remote_dict(d["onSuccess"]) if "onSuccess" in d else None,
                             OnQuasiTransferCompleted.from_remote_dict(d["onFailure"]) if "onFailure" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return QuasiTransfer(d["id"],
                             d["url"],
                             d["description"] if "description" in d else None,
                             Creator.from_dict(d["creator"]),
                             d["foreign_id"] if "foreign_id" in d else None,
                             d["foreign_data"] if "foreign_data" in d else None,
                             UTCDateTime.from_dict(d["created_time"]),
                             UTCDateTime.from_dict(d["completed_time"]) if "completed_time" in d else None,
                             H1Descriptor.from_dict(d["h1_descriptor"]) if "h1_descriptor" in d else None,
                             SecurePay.from_dict(d["secure_pay"]),
                             Amount.from_dict(d["amount"]) if "amount" in d else None,
                             Sending.from_string(d["sending"]),
                             QuasiTransferStatus.from_dict(d["status"]),
                             Source.from_dict(d["source"]),
                             Destination.from_dict(d["destination"]) if "destination" in d else None,
                             Fees.from_dict(d["fees"]),
                             Expire.from_dict(d["expire"]) if "expire" in d else None,
                             OnQuasiTransferCompleted.from_dict(d["on_success"]) if "on_success" in d else None,
                             OnQuasiTransferCompleted.from_dict(d["on_failure"]) if "on_failure" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("QuasiTransfer(id=" + self.id + 
                              ", url=" + self.url + 
                              ", description=" + str(self.description) + 
                              ", creator=" + repr(self.creator) + 
                              ", foreign_id=" + str(self.foreign_id) + 
                              ", foreign_data=" + str(self.foreign_data) + 
                              ", created_time=" + repr(self.created_time) + 
                              ", completed_time=" + repr(self.completed_time) + 
                              ", h1_descriptor=" + repr(self.h1_descriptor) + 
                              ", secure_pay=" + repr(self.secure_pay) + 
                              ", amount=" + repr(self.amount) + 
                              ", sending=" + repr(self.sending) + 
                              ", status=" + repr(self.status) + 
                              ", source=" + repr(self.source) + 
                              ", destination=" + repr(self.destination) + 
                              ", fees=" + repr(self.fees) + 
                              ", expire=" + repr(self.expire) + 
                              ", on_success=" + repr(self.on_success) + 
                              ", on_failure=" + repr(self.on_failure) + ")")

class Transfer(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str],
                 created_time: UTCDateTime,
                 completed_time: Optional[UTCDateTime],
                 h1_descriptor: Optional[H1Descriptor],
                 sending: Sending,
                 source: Source,
                 destination: Destination,
                 fees: Fees,
                 attempt: LightAttempt,
                 amount: Amount,
                 status: TransferStatus):
        self._type = "Transfer" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data
        self.created_time = created_time
        self.completed_time = completed_time
        self.h1_descriptor = h1_descriptor
        self.sending = sending
        self.source = source
        self.destination = destination
        self.fees = fees
        self.attempt = attempt
        self.amount = amount
        self.status = status

    @staticmethod
    def _type(): 
        return "Transfer"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Transfer.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('completedTime', self.completed_time.__to_remote_dict()),
            ('h1Descriptor', self.h1_descriptor.__to_remote_dict()),
            ('sending', str(self.sending)),
            ('source', self.source.__to_remote_dict()),
            ('destination', self.destination.__to_remote_dict()),
            ('fees', self.fees.__to_remote_dict()),
            ('attempt', self.attempt.__to_remote_dict()),
            ('amount', self.amount.__to_remote_dict()),
            ('status', self.status.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data),
            ('created_time', self.created_time.to_dict()),
            ('completed_time', self.completed_time.to_dict()),
            ('h1_descriptor', self.h1_descriptor.to_dict()),
            ('sending', str(self.sending)),
            ('source', self.source.to_dict()),
            ('destination', self.destination.to_dict()),
            ('fees', self.fees.to_dict()),
            ('attempt', self.attempt.to_dict()),
            ('amount', self.amount.to_dict()),
            ('status', self.status.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Transfer(d["id"],
                        d["url"],
                        d["description"] if "description" in d else None,
                        Creator.from_remote_dict(d["creator"]),
                        d["foreignId"] if "foreignId" in d else None,
                        d["foreignData"] if "foreignData" in d else None,
                        UTCDateTime.from_remote_dict(d["createdTime"]),
                        UTCDateTime.from_remote_dict(d["completedTime"]) if "completedTime" in d else None,
                        H1Descriptor.from_remote_dict(d["h1Descriptor"]) if "h1Descriptor" in d else None,
                        Sending.from_string(d["sending"]),
                        Source.from_remote_dict(d["source"]),
                        Destination.from_remote_dict(d["destination"]),
                        Fees.from_remote_dict(d["fees"]),
                        LightAttempt.from_remote_dict(d["attempt"]),
                        Amount.from_remote_dict(d["amount"]),
                        TransferStatus.from_remote_dict(d["status"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Transfer(d["id"],
                        d["url"],
                        d["description"] if "description" in d else None,
                        Creator.from_dict(d["creator"]),
                        d["foreign_id"] if "foreign_id" in d else None,
                        d["foreign_data"] if "foreign_data" in d else None,
                        UTCDateTime.from_dict(d["created_time"]),
                        UTCDateTime.from_dict(d["completed_time"]) if "completed_time" in d else None,
                        H1Descriptor.from_dict(d["h1_descriptor"]) if "h1_descriptor" in d else None,
                        Sending.from_string(d["sending"]),
                        Source.from_dict(d["source"]),
                        Destination.from_dict(d["destination"]),
                        Fees.from_dict(d["fees"]),
                        LightAttempt.from_dict(d["attempt"]),
                        Amount.from_dict(d["amount"]),
                        TransferStatus.from_dict(d["status"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Transfer(id=" + self.id + 
                         ", url=" + self.url + 
                         ", description=" + str(self.description) + 
                         ", creator=" + repr(self.creator) + 
                         ", foreign_id=" + str(self.foreign_id) + 
                         ", foreign_data=" + str(self.foreign_data) + 
                         ", created_time=" + repr(self.created_time) + 
                         ", completed_time=" + repr(self.completed_time) + 
                         ", h1_descriptor=" + repr(self.h1_descriptor) + 
                         ", sending=" + repr(self.sending) + 
                         ", source=" + repr(self.source) + 
                         ", destination=" + repr(self.destination) + 
                         ", fees=" + repr(self.fees) + 
                         ", attempt=" + repr(self.attempt) + 
                         ", amount=" + repr(self.amount) + 
                         ", status=" + repr(self.status) + ")")

class Wallet(TransactionParent):
    def __init__(self,
                 id: str,
                 url: str,
                 description: Optional[str],
                 creator: Creator,
                 foreign_id: Optional[str],
                 foreign_data: Optional[str],
                 created_time: UTCDateTime,
                 name: str,
                 is_main: bool,
                 mars: Mars,
                 main_pocket: Pocket,
                 man: Man):
        self._type = "Wallet" 
        super()
        self.id = id
        self.url = url
        self.description = description
        self.creator = creator
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data
        self.created_time = created_time
        self.name = name
        self.is_main = is_main
        self.mars = mars
        self.main_pocket = main_pocket
        self.man = man

    @staticmethod
    def _type(): 
        return "Wallet"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Wallet.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.__to_remote_dict()),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('name', self.name),
            ('isMain', self.is_main),
            ('mars', self.mars.__to_remote_dict()),
            ('mainPocket', self.main_pocket.__to_remote_dict()),
            ('man', self.man.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('description', self.description),
            ('creator', self.creator.to_dict()),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data),
            ('created_time', self.created_time.to_dict()),
            ('name', self.name),
            ('is_main', self.is_main),
            ('mars', self.mars.to_dict()),
            ('main_pocket', self.main_pocket.to_dict()),
            ('man', self.man.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Wallet(d["id"],
                      d["url"],
                      d["description"] if "description" in d else None,
                      Creator.from_remote_dict(d["creator"]),
                      d["foreignId"] if "foreignId" in d else None,
                      d["foreignData"] if "foreignData" in d else None,
                      UTCDateTime.from_remote_dict(d["createdTime"]),
                      d["name"],
                      d["isMain"],
                      Mars.from_remote_dict(d["mars"]),
                      Pocket.from_remote_dict(d["mainPocket"]),
                      Man.from_remote_dict(d["man"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Wallet(d["id"],
                      d["url"],
                      d["description"] if "description" in d else None,
                      Creator.from_dict(d["creator"]),
                      d["foreign_id"] if "foreign_id" in d else None,
                      d["foreign_data"] if "foreign_data" in d else None,
                      UTCDateTime.from_dict(d["created_time"]),
                      d["name"],
                      d["is_main"],
                      Mars.from_dict(d["mars"]),
                      Pocket.from_dict(d["main_pocket"]),
                      Man.from_dict(d["man"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Wallet(id=" + self.id + 
                       ", url=" + self.url + 
                       ", description=" + str(self.description) + 
                       ", creator=" + repr(self.creator) + 
                       ", foreign_id=" + str(self.foreign_id) + 
                       ", foreign_data=" + str(self.foreign_data) + 
                       ", created_time=" + repr(self.created_time) + 
                       ", name=" + self.name + 
                       ", is_main=" + str(self.is_main) + 
                       ", mars=" + repr(self.mars) + 
                       ", main_pocket=" + repr(self.main_pocket) + 
                       ", man=" + repr(self.man) + ")")