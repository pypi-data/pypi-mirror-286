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


class TransactionStatus(ABC):
    def is_successful(self):
        return self._type == Successful._type()

    def is_failure(self):
        return self._type == Failure._type()

    def as_successful(self):
        if self.is_successful():
            return self
        else:
            return None

    def as_failure(self):
        if self.is_failure():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return TransactionStatus.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Successful._type(): return Successful.from_remote_dict(d)
        elif ty == Failure._type(): return Failure.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransactionStatus'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Successful._type(): return Successful.from_dict(d)
        elif ty == Failure._type(): return Failure.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransactionStatus'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class Successful(TransactionStatus):
    def __init__(self):
        self._type = "Successful" 
        super()

    @staticmethod
    def _type(): 
        return "Successful"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Successful.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Successful()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Successful()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Successful"

class Failure(TransactionStatus):
    def __init__(self, is_cancelled: bool):
        self._type = "Failure" 
        super()
        self.is_cancelled = is_cancelled

    @staticmethod
    def _type(): 
        return "Failure"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Failure.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('isCancelled', self.is_cancelled)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('is_cancelled', self.is_cancelled)])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Failure(d["isCancelled"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Failure(d["is_cancelled"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Failure(is_cancelled=" + str(self.is_cancelled) + ")"