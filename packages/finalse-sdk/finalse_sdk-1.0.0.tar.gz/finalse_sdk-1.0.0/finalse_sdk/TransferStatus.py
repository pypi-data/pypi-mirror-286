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
from finalse_sdk.Cancelled import Cancelled
from finalse_sdk.LocalizedText import LocalizedText
from typing import Dict
from typing import Optional
import json


class TransferStatus(ABC):
    def is_waiting_to_start(self):
        return self._type == WaitingToStart._type()

    def is_starting(self):
        return self._type == Starting._type()

    def is_started(self):
        return self._type == Started._type()

    def is_processing(self):
        return self._type == Processing._type()

    def is_completing(self):
        return self._type == Completing._type()

    def is_failure(self):
        return self._type == Failure._type()

    def is_successful(self):
        return self._type == Successful._type()

    def as_waiting_to_start(self):
        if self.is_waiting_to_start():
            return self
        else:
            return None

    def as_starting(self):
        if self.is_starting():
            return self
        else:
            return None

    def as_started(self):
        if self.is_started():
            return self
        else:
            return None

    def as_processing(self):
        if self.is_processing():
            return self
        else:
            return None

    def as_completing(self):
        if self.is_completing():
            return self
        else:
            return None

    def as_failure(self):
        if self.is_failure():
            return self
        else:
            return None

    def as_successful(self):
        if self.is_successful():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return TransferStatus.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == WaitingToStart._type(): return WaitingToStart.from_remote_dict(d)
        elif ty == Starting._type(): return Starting.from_remote_dict(d);
        elif ty == Started._type(): return Started.from_remote_dict(d);
        elif ty == Processing._type(): return Processing.from_remote_dict(d);
        elif ty == Completing._type(): return Completing.from_remote_dict(d);
        elif ty == Failure._type(): return Failure.from_remote_dict(d);
        elif ty == Successful._type(): return Successful.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransferStatus'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == WaitingToStart._type(): return WaitingToStart.from_dict(d)
        elif ty == Starting._type(): return Starting.from_dict(d);
        elif ty == Started._type(): return Started.from_dict(d);
        elif ty == Processing._type(): return Processing.from_dict(d);
        elif ty == Completing._type(): return Completing.from_dict(d);
        elif ty == Failure._type(): return Failure.from_dict(d);
        elif ty == Successful._type(): return Successful.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'TransferStatus'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class WaitingToStart(TransferStatus):
    def __init__(self):
        self._type = "WaitingToStart" 
        super()

    @staticmethod
    def _type(): 
        return "WaitingToStart"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return WaitingToStart.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return WaitingToStart()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return WaitingToStart()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "WaitingToStart"

class Starting(TransferStatus):
    def __init__(self):
        self._type = "Starting" 
        super()

    @staticmethod
    def _type(): 
        return "Starting"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Starting.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Starting()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Starting()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Starting"

class Started(TransferStatus):
    def __init__(self):
        self._type = "Started" 
        super()

    @staticmethod
    def _type(): 
        return "Started"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Started.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Started()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Started()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Started"

class Processing(TransferStatus):
    def __init__(self, reason: LocalizedText):
        self._type = "Processing" 
        super()
        self.reason = reason

    @staticmethod
    def _type(): 
        return "Processing"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Processing.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('reason', self.reason.__to_remote_dict())]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('reason', self.reason.to_dict())])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Processing(LocalizedText.from_remote_dict(d["reason"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Processing(LocalizedText.from_dict(d["reason"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Processing(reason=" + repr(self.reason) + ")"

class Completing(TransferStatus):
    def __init__(self):
        self._type = "Completing" 
        super()

    @staticmethod
    def _type(): 
        return "Completing"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Completing.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Completing()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Completing()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Completing"

class Failure(TransferStatus):
    def __init__(self, reason: LocalizedText, cancelled: Optional[Cancelled]):
        self._type = "Failure" 
        super()
        self.reason = reason
        self.cancelled = cancelled

    @staticmethod
    def _type(): 
        return "Failure"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Failure.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('reason', self.reason.__to_remote_dict()),
            ('cancelled', self.cancelled.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('reason', self.reason.to_dict()),
            ('cancelled', self.cancelled.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Failure(LocalizedText.from_remote_dict(d["reason"]),
                       Cancelled.from_remote_dict(d["cancelled"]) if "cancelled" in d else None)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Failure(LocalizedText.from_dict(d["reason"]),
                       Cancelled.from_dict(d["cancelled"]) if "cancelled" in d else None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Failure(reason=" + repr(self.reason) + 
                        ", cancelled=" + repr(self.cancelled) + ")")

class Successful(TransferStatus):
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