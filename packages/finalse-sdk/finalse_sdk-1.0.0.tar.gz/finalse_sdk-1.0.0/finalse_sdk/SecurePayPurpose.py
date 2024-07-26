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
from finalse_sdk.PurchaseLabel import PurchaseLabel
from typing import Dict
import json


class SecurePayPurpose(ABC):
    def is_send(self):
        return self._type == Send._type()

    def is_receive(self):
        return self._type == Receive._type()

    def is_purchase(self):
        return self._type == Purchase._type()

    def as_send(self):
        if self.is_send():
            return self
        else:
            return None

    def as_receive(self):
        if self.is_receive():
            return self
        else:
            return None

    def as_purchase(self):
        if self.is_purchase():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return SecurePayPurpose.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Send._type(): return Send.from_remote_dict(d)
        elif ty == Receive._type(): return Receive.from_remote_dict(d);
        elif ty == Purchase._type(): return Purchase.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'SecurePayPurpose'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == Send._type(): return Send.from_dict(d)
        elif ty == Receive._type(): return Receive.from_dict(d);
        elif ty == Purchase._type(): return Purchase.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'SecurePayPurpose'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class Send(SecurePayPurpose):
    def __init__(self):
        self._type = "Send" 
        super()

    @staticmethod
    def _type(): 
        return "Send"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Send.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Send()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Send()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Send"

class Receive(SecurePayPurpose):
    def __init__(self):
        self._type = "Receive" 
        super()

    @staticmethod
    def _type(): 
        return "Receive"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Receive.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Receive()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Receive()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Receive"

class Purchase(SecurePayPurpose):
    def __init__(self, label: PurchaseLabel):
        self._type = "Purchase" 
        super()
        self.label = label

    @staticmethod
    def _type(): 
        return "Purchase"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Purchase.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('label', str(self.label))]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('label', str(self.label))])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Purchase(PurchaseLabel.from_string(d["label"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Purchase(PurchaseLabel.from_string(d["label"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Purchase(label=" + repr(self.label) + ")"