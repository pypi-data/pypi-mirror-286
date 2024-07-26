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
from finalse_sdk.Dc import Dc
from finalse_sdk.H1 import H1
from finalse_sdk.MoneyAccount import MoneyAccount
from finalse_sdk.TransactionDetails import TransactionDetails
from finalse_sdk.TransactionParent import TransactionParent
from finalse_sdk.TransactionStatus import TransactionStatus
from finalse_sdk.TransactionWalletView import TransactionWalletView
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
from typing import Optional
import json


class Transaction:
    def __init__(self,
                 id: str,
                 url: str,
                 created_time: UTCDateTime,
                 h1: H1,
                 details: TransactionDetails,
                 dc: Dc,
                 parent: TransactionParent,
                 source: MoneyAccount,
                 destination: MoneyAccount,
                 amount: Amount,
                 status: TransactionStatus,
                 wallet: TransactionWalletView,
                 description: Optional[str],
                 foreign_data: Optional[str]):
        self._type = "Transaction" 
        self.id = id
        self.url = url
        self.created_time = created_time
        self.h1 = h1
        self.details = details
        self.dc = dc
        self.parent = parent
        self.source = source
        self.destination = destination
        self.amount = amount
        self.status = status
        self.wallet = wallet
        self.description = description
        self.foreign_data = foreign_data

    @staticmethod
    def _type(): 
        return "Transaction"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Transaction.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('h1', self.h1.__to_remote_dict()),
            ('details', self.details.__to_remote_dict()),
            ('dc', str(self.dc)),
            ('parent', self.parent.__to_remote_dict()),
            ('source', self.source.__to_remote_dict()),
            ('destination', self.destination.__to_remote_dict()),
            ('amount', self.amount.__to_remote_dict()),
            ('status', self.status.__to_remote_dict()),
            ('wallet', self.wallet.__to_remote_dict()),
            ('description', self.description),
            ('foreignData', self.foreign_data)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('created_time', self.created_time.to_dict()),
            ('h1', self.h1.to_dict()),
            ('details', self.details.to_dict()),
            ('dc', str(self.dc)),
            ('parent', self.parent.to_dict()),
            ('source', self.source.to_dict()),
            ('destination', self.destination.to_dict()),
            ('amount', self.amount.to_dict()),
            ('status', self.status.to_dict()),
            ('wallet', self.wallet.to_dict()),
            ('description', self.description),
            ('foreign_data', self.foreign_data)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Transaction(d["id"],
                           d["url"],
                           UTCDateTime.from_remote_dict(d["createdTime"]),
                           H1.from_remote_dict(d["h1"]),
                           TransactionDetails.from_remote_dict(d["details"]),
                           Dc.from_string(d["dc"]),
                           TransactionParent.from_remote_dict(d["parent"]),
                           MoneyAccount.from_remote_dict(d["source"]),
                           MoneyAccount.from_remote_dict(d["destination"]),
                           Amount.from_remote_dict(d["amount"]),
                           TransactionStatus.from_remote_dict(d["status"]),
                           TransactionWalletView.from_remote_dict(d["wallet"]),
                           d["description"] if "description" in d else None,
                           d["foreignData"] if "foreignData" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Transaction(d["id"],
                           d["url"],
                           UTCDateTime.from_dict(d["created_time"]),
                           H1.from_dict(d["h1"]),
                           TransactionDetails.from_dict(d["details"]),
                           Dc.from_string(d["dc"]),
                           TransactionParent.from_dict(d["parent"]),
                           MoneyAccount.from_dict(d["source"]),
                           MoneyAccount.from_dict(d["destination"]),
                           Amount.from_dict(d["amount"]),
                           TransactionStatus.from_dict(d["status"]),
                           TransactionWalletView.from_dict(d["wallet"]),
                           d["description"] if "description" in d else None,
                           d["foreign_data"] if "foreign_data" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Transaction(id=" + self.id + 
                            ", url=" + self.url + 
                            ", created_time=" + repr(self.created_time) + 
                            ", h1=" + repr(self.h1) + 
                            ", details=" + repr(self.details) + 
                            ", dc=" + repr(self.dc) + 
                            ", parent=" + repr(self.parent) + 
                            ", source=" + repr(self.source) + 
                            ", destination=" + repr(self.destination) + 
                            ", amount=" + repr(self.amount) + 
                            ", status=" + repr(self.status) + 
                            ", wallet=" + repr(self.wallet) + 
                            ", description=" + str(self.description) + 
                            ", foreign_data=" + str(self.foreign_data) + ")")