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
from finalse_sdk.AuthAccessPermissionSimpleName import AuthAccessPermissionSimpleName
from typing import Dict
import json


class AuthAccessPermission(ABC):
    def is_simple(self):
        return self._type == Simple._type()

    def is_complex(self):
        return self._type == Complex._type()

    def as_simple(self):
        if self.is_simple():
            return self
        else:
            return None

    def as_complex(self):
        if self.is_complex():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return AuthAccessPermission.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Simple._type(): return Simple.from_remote_dict(d)
        elif ty == Complex._type(): return Complex.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'AuthAccessPermission'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Simple._type(): return Simple.from_dict(d)
        elif ty == Complex._type(): return Complex.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'AuthAccessPermission'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class Simple(AuthAccessPermission):
    def __init__(self, name: AuthAccessPermissionSimpleName):
        self._type = "Simple" 
        super()
        self.name = name

    @staticmethod
    def _type(): 
        return "Simple"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Simple.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('name', str(self.name))]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('name', str(self.name))])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Simple(AuthAccessPermissionSimpleName.from_string(d["name"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Simple(AuthAccessPermissionSimpleName.from_string(d["name"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Simple(name=" + repr(self.name) + ")"

class Complex(AuthAccessPermission):
    def __init__(self):
        self._type = "Complex" 
        super()

    @staticmethod
    def _type(): 
        return "Complex"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Complex.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Complex()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Complex()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Complex"