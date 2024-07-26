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
from finalse_sdk.Creator import Creator
from finalse_sdk.Man import Man
from finalse_sdk.Mars import Mars
from finalse_sdk.Pocket import Pocket
from finalse_sdk.UTCDateTime import UTCDateTime
from typing import Dict
from typing import Optional
import json


class Wallet:
    def __init__(self,
                 id: str,
                 url: str,
                 creator: Creator,
                 created_time: UTCDateTime,
                 description: Optional[str],
                 foreign_id: Optional[str],
                 foreign_data: Optional[str],
                 name: str,
                 is_main: bool,
                 mars: Mars,
                 main_pocket: Pocket,
                 man: Man):
        self._type = "Wallet" 
        self.id = id
        self.url = url
        self.creator = creator
        self.created_time = created_time
        self.description = description
        self.foreign_id = foreign_id
        self.foreign_data = foreign_data
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
            ('creator', self.creator.__to_remote_dict()),
            ('createdTime', self.created_time.__to_remote_dict()),
            ('description', self.description),
            ('foreignId', self.foreign_id),
            ('foreignData', self.foreign_data),
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
            ('creator', self.creator.to_dict()),
            ('created_time', self.created_time.to_dict()),
            ('description', self.description),
            ('foreign_id', self.foreign_id),
            ('foreign_data', self.foreign_data),
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
                      Creator.from_remote_dict(d["creator"]),
                      UTCDateTime.from_remote_dict(d["createdTime"]),
                      d["description"] if "description" in d else None,
                      d["foreignId"] if "foreignId" in d else None,
                      d["foreignData"] if "foreignData" in d else None,
                      d["name"],
                      d["isMain"],
                      Mars.from_remote_dict(d["mars"]),
                      Pocket.from_remote_dict(d["mainPocket"]),
                      Man.from_remote_dict(d["man"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Wallet(d["id"],
                      d["url"],
                      Creator.from_dict(d["creator"]),
                      UTCDateTime.from_dict(d["created_time"]),
                      d["description"] if "description" in d else None,
                      d["foreign_id"] if "foreign_id" in d else None,
                      d["foreign_data"] if "foreign_data" in d else None,
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
                       ", creator=" + repr(self.creator) + 
                       ", created_time=" + repr(self.created_time) + 
                       ", description=" + str(self.description) + 
                       ", foreign_id=" + str(self.foreign_id) + 
                       ", foreign_data=" + str(self.foreign_data) + 
                       ", name=" + self.name + 
                       ", is_main=" + str(self.is_main) + 
                       ", mars=" + repr(self.mars) + 
                       ", main_pocket=" + repr(self.main_pocket) + 
                       ", man=" + repr(self.man) + ")")