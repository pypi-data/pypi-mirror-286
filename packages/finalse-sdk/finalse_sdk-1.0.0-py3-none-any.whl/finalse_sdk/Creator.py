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
import json


class Creator(ABC):
    def is_ui(self):
        return self._type == Ui._type()

    def is_api(self):
        return self._type == Api._type()

    def as_ui(self):
        if self.is_ui():
            return self
        else:
            return None

    def as_api(self):
        if self.is_api():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Creator.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Ui._type(): return Ui.from_remote_dict(d)
        elif ty == Api._type(): return Api.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'Creator'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Ui._type(): return Ui.from_dict(d)
        elif ty == Api._type(): return Api.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'Creator'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class Ui(Creator):
    def __init__(self, account_id: str, person_id: str):
        self._type = "Ui" 
        super()
        self.account_id = account_id
        self.person_id = person_id

    @staticmethod
    def _type(): 
        return "Ui"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Ui.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('accountId', self.account_id),
            ('personId', self.person_id)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('account_id', self.account_id),
            ('person_id', self.person_id)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Ui(d["accountId"],
                  d["personId"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Ui(d["account_id"],
                  d["person_id"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Ui(account_id=" + self.account_id + 
                   ", person_id=" + self.person_id + ")")

class Api(Creator):
    def __init__(self, account_id: str, auth_access_id: str):
        self._type = "Api" 
        super()
        self.account_id = account_id
        self.auth_access_id = auth_access_id

    @staticmethod
    def _type(): 
        return "Api"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Api.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('accountId', self.account_id),
            ('authAccessId', self.auth_access_id)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('account_id', self.account_id),
            ('auth_access_id', self.auth_access_id)
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Api(d["accountId"],
                   d["authAccessId"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Api(d["account_id"],
                   d["auth_access_id"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Api(account_id=" + self.account_id + 
                    ", auth_access_id=" + self.auth_access_id + ")")