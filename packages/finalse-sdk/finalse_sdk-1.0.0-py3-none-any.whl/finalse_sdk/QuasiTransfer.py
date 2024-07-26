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
from finalse_sdk.Creator import Creator
from finalse_sdk.Destination import Destination
from finalse_sdk.Expire import Expire
from finalse_sdk.Fees import Fees
from finalse_sdk.H1Descriptor import H1Descriptor
from finalse_sdk.OnQuasiTransferCompleted import OnQuasiTransferCompleted
from finalse_sdk.QuasiTransferStatus import QuasiTransferStatus
from finalse_sdk.SecurePay import SecurePay
from finalse_sdk.Sending import Sending
from finalse_sdk.Source import Source
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
from typing import Optional
import json


class QuasiTransfer:
    def __init__(self,
                 id: str,
                 url: str,
                 creator: Creator,
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
                 on_failure: Optional[OnQuasiTransferCompleted],
                 description: Optional[str],
                 foreign_id: Optional[str],
                 foreign_data: Optional[str]):
        self._type = "QuasiTransfer" 
        self.id = id
        self.url = url
        self.creator = creator
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
        self.description = description
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data

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
            ('creator', self.creator.__to_remote_dict()),
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
            ('onFailure', self.on_failure.__to_remote_dict()),
            ('description', self.description),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('creator', self.creator.to_dict()),
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
            ('on_failure', self.on_failure.to_dict()),
            ('description', self.description),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return QuasiTransfer(d["id"],
                             d["url"],
                             Creator.from_remote_dict(d["creator"]),
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
                             OnQuasiTransferCompleted.from_remote_dict(d["onFailure"]) if "onFailure" in d else None,
                             d["description"] if "description" in d else None,
                             d["foreignId"] if "foreignId" in d else None,
                             d["foreignData"] if "foreignData" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return QuasiTransfer(d["id"],
                             d["url"],
                             Creator.from_dict(d["creator"]),
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
                             OnQuasiTransferCompleted.from_dict(d["on_failure"]) if "on_failure" in d else None,
                             d["description"] if "description" in d else None,
                             d["foreign_id"] if "foreign_id" in d else None,
                             d["foreign_data"] if "foreign_data" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("QuasiTransfer(id=" + self.id + 
                              ", url=" + self.url + 
                              ", creator=" + repr(self.creator) + 
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
                              ", on_failure=" + repr(self.on_failure) + 
                              ", description=" + str(self.description) + 
                              ", foreign_id=" + str(self.foreign_id) + 
                              ", foreign_data=" + str(self.foreign_data) + ")")