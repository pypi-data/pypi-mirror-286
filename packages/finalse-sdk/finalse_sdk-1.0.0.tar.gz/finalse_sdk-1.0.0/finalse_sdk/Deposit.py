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
from finalse_sdk.DepositStatus import DepositStatus
from finalse_sdk.Destination import Destination
from finalse_sdk.Fees import Fees
from finalse_sdk.H1Descriptor import H1Descriptor
from finalse_sdk.LightAttempt import LightAttempt
from finalse_sdk.Sending import Sending
from finalse_sdk.Source import Source
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
from typing import Optional
import json


class Deposit:
    def __init__(self,
                 id: str,
                 url: str,
                 created_time: UTCDateTime,
                 creator: Creator,
                 completed_time: Optional[UTCDateTime],
                 h1_descriptor: Optional[H1Descriptor],
                 source: Source,
                 destination: Destination,
                 fees: Fees,
                 attempt: LightAttempt,
                 amount: Amount,
                 sending: Sending,
                 status: DepositStatus,
                 description: Optional[str],
                 foreign_id: Optional[str],
                 foreign_data: Optional[str]):
        self._type = "Deposit" 
        self.id = id
        self.url = url
        self.created_time = created_time
        self.creator = creator
        self.completed_time = completed_time
        self.h1_descriptor = h1_descriptor
        self.source = source
        self.destination = destination
        self.fees = fees
        self.attempt = attempt
        self.amount = amount
        self.sending = sending
        self.status = status
        self.description = description
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data

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
            ('createdTime', self.created_time.__to_remote_dict()),
            ('creator', self.creator.__to_remote_dict()),
            ('completedTime', self.completed_time.__to_remote_dict()),
            ('h1Descriptor', self.h1_descriptor.__to_remote_dict()),
            ('source', self.source.__to_remote_dict()),
            ('destination', self.destination.__to_remote_dict()),
            ('fees', self.fees.__to_remote_dict()),
            ('attempt', self.attempt.__to_remote_dict()),
            ('amount', self.amount.__to_remote_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.__to_remote_dict()),
            ('description', self.description),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('created_time', self.created_time.to_dict()),
            ('creator', self.creator.to_dict()),
            ('completed_time', self.completed_time.to_dict()),
            ('h1_descriptor', self.h1_descriptor.to_dict()),
            ('source', self.source.to_dict()),
            ('destination', self.destination.to_dict()),
            ('fees', self.fees.to_dict()),
            ('attempt', self.attempt.to_dict()),
            ('amount', self.amount.to_dict()),
            ('sending', str(self.sending)),
            ('status', self.status.to_dict()),
            ('description', self.description),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Deposit(d["id"],
                       d["url"],
                       UTCDateTime.from_remote_dict(d["createdTime"]),
                       Creator.from_remote_dict(d["creator"]),
                       UTCDateTime.from_remote_dict(d["completedTime"]) if "completedTime" in d else None,
                       H1Descriptor.from_remote_dict(d["h1Descriptor"]) if "h1Descriptor" in d else None,
                       Source.from_remote_dict(d["source"]),
                       Destination.from_remote_dict(d["destination"]),
                       Fees.from_remote_dict(d["fees"]),
                       LightAttempt.from_remote_dict(d["attempt"]),
                       Amount.from_remote_dict(d["amount"]),
                       Sending.from_string(d["sending"]),
                       DepositStatus.from_remote_dict(d["status"]),
                       d["description"] if "description" in d else None,
                       d["foreignId"] if "foreignId" in d else None,
                       d["foreignData"] if "foreignData" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Deposit(d["id"],
                       d["url"],
                       UTCDateTime.from_dict(d["created_time"]),
                       Creator.from_dict(d["creator"]),
                       UTCDateTime.from_dict(d["completed_time"]) if "completed_time" in d else None,
                       H1Descriptor.from_dict(d["h1_descriptor"]) if "h1_descriptor" in d else None,
                       Source.from_dict(d["source"]),
                       Destination.from_dict(d["destination"]),
                       Fees.from_dict(d["fees"]),
                       LightAttempt.from_dict(d["attempt"]),
                       Amount.from_dict(d["amount"]),
                       Sending.from_string(d["sending"]),
                       DepositStatus.from_dict(d["status"]),
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
        return ("Deposit(id=" + self.id + 
                        ", url=" + self.url + 
                        ", created_time=" + repr(self.created_time) + 
                        ", creator=" + repr(self.creator) + 
                        ", completed_time=" + repr(self.completed_time) + 
                        ", h1_descriptor=" + repr(self.h1_descriptor) + 
                        ", source=" + repr(self.source) + 
                        ", destination=" + repr(self.destination) + 
                        ", fees=" + repr(self.fees) + 
                        ", attempt=" + repr(self.attempt) + 
                        ", amount=" + repr(self.amount) + 
                        ", sending=" + repr(self.sending) + 
                        ", status=" + repr(self.status) + 
                        ", description=" + str(self.description) + 
                        ", foreign_id=" + str(self.foreign_id) + 
                        ", foreign_data=" + str(self.foreign_data) + ")")