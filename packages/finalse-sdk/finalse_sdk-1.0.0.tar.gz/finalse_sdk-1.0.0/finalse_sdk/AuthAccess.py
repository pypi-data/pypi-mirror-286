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
from finalse_sdk.AuthAccessPermission import AuthAccessPermission
from finalse_sdk.Creator import Creator
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
from typing import Optional
import json


class AuthAccess:
    def __init__(self,
                 id: str,
                 url: str,
                 created_time: UTCDateTime,
                 name: str,
                 token: str,
                 permission: AuthAccessPermission,
                 secret_key: str,
                 is_enabled: bool,
                 creator: Creator,
                 description: Optional[str],
                 foreign_id: Optional[str],
                 foreign_data: Optional[str]):
        self._type = "AuthAccess" 
        self.id = id
        self.url = url
        self.created_time = created_time
        self.name = name
        self.token = token
        self.permission = permission
        self.secret_key = secret_key
        self.is_enabled = is_enabled
        self.creator = creator
        self.description = description
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data

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
            ('createdTime', self.created_time.__to_remote_dict()),
            ('name', self.name),
            ('token', self.token),
            ('permission', self.permission.__to_remote_dict()),
            ('secretKey', self.secret_key),
            ('isEnabled', self.is_enabled),
            ('creator', self.creator.__to_remote_dict()),
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
            ('name', self.name),
            ('token', self.token),
            ('permission', self.permission.to_dict()),
            ('secret_key', self.secret_key),
            ('is_enabled', self.is_enabled),
            ('creator', self.creator.to_dict()),
            ('description', self.description),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return AuthAccess(d["id"],
                          d["url"],
                          UTCDateTime.from_remote_dict(d["createdTime"]),
                          d["name"],
                          d["token"],
                          AuthAccessPermission.from_remote_dict(d["permission"]),
                          d["secretKey"],
                          d["isEnabled"],
                          Creator.from_remote_dict(d["creator"]),
                          d["description"] if "description" in d else None,
                          d["foreignId"] if "foreignId" in d else None,
                          d["foreignData"] if "foreignData" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return AuthAccess(d["id"],
                          d["url"],
                          UTCDateTime.from_dict(d["created_time"]),
                          d["name"],
                          d["token"],
                          AuthAccessPermission.from_dict(d["permission"]),
                          d["secret_key"],
                          d["is_enabled"],
                          Creator.from_dict(d["creator"]),
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
        return ("AuthAccess(id=" + self.id + 
                           ", url=" + self.url + 
                           ", created_time=" + repr(self.created_time) + 
                           ", name=" + self.name + 
                           ", token=" + self.token + 
                           ", permission=" + repr(self.permission) + 
                           ", secret_key=******" + 
                           ", is_enabled=" + str(self.is_enabled) + 
                           ", creator=" + repr(self.creator) + 
                           ", description=" + str(self.description) + 
                           ", foreign_id=" + str(self.foreign_id) + 
                           ", foreign_data=" + str(self.foreign_data) + ")")