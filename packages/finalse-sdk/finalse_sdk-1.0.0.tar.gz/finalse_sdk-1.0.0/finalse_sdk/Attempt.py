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
from finalse_sdk.AttemptParentType import AttemptParentType
from finalse_sdk.AttemptStatus import AttemptStatus
from finalse_sdk.AttemptValidation import AttemptValidation
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
from typing import List
import json


class Attempt:
    def __init__(self,
                 id: str,
                 url: str,
                 created_time: UTCDateTime,
                 parent_type: AttemptParentType,
                 parent_id: str,
                 status: AttemptStatus,
                 validations: list[AttemptValidation]):
        self._type = "Attempt" 
        self.id = id
        self.url = url
        self.created_time = created_time
        self.parent_type = parent_type
        self.parent_id = parent_id
        self.status = status
        self.validations = validations

    @staticmethod
    def _type(): 
        return "Attempt"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Attempt.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('url', self.url),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('parentType', str(self.parent_type)),
            ('parentId', self.parent_id),
            ('status', self.status.__to_remote_dict()),
            ('validations', list(map(lambda el: el.__to_remote_dict(), self.validations)))
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('url', self.url),
            ('created_time', self.created_time.to_dict()),
            ('parent_type', str(self.parent_type)),
            ('parent_id', self.parent_id),
            ('status', self.status.to_dict()),
            ('validations', list(map(lambda el: el.to_dict(), self.validations)))
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Attempt(d["id"],
                       d["url"],
                       UTCDateTime.from_remote_dict(d["createdTime"]),
                       AttemptParentType.from_string(d["parentType"]),
                       d["parentId"],
                       AttemptStatus.from_remote_dict(d["status"]),
                       list(map(lambda el: AttemptValidation.from_remote_dict(el), d["validations"])))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Attempt(d["id"],
                       d["url"],
                       UTCDateTime.from_dict(d["created_time"]),
                       AttemptParentType.from_string(d["parent_type"]),
                       d["parent_id"],
                       AttemptStatus.from_dict(d["status"]),
                       list(map(lambda el: AttemptValidation.from_dict(el), d["validations"])))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Attempt(id=" + self.id + 
                        ", url=" + self.url + 
                        ", created_time=" + repr(self.created_time) + 
                        ", parent_type=" + repr(self.parent_type) + 
                        ", parent_id=" + self.parent_id + 
                        ", status=" + repr(self.status) + 
                        ", validations=" + repr(self.validations) + ")")