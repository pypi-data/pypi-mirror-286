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
from finalse_sdk.Expire import Expire
from finalse_sdk.LocalizedText import LocalizedText
from finalse_sdk.LocalizedVariableText import LocalizedVariableText
from finalse_sdk.MfaProcessConfirm import MfaProcessConfirm
from finalse_sdk.MoneyAccountProvider import MoneyAccountProvider
from finalse_sdk.Otp import Otp
from typing import Dict
import json


class MfaProcess(ABC):
    def is_not_required(self):
        return self._type == NotRequired._type()

    def is_waiting_to_start(self):
        return self._type == WaitingToStart._type()

    def is_starting(self):
        return self._type == Starting._type()

    def is_one_time_password_required(self):
        return self._type == OneTimePasswordRequired._type()

    def is_secret_code_required(self):
        return self._type == SecretCodeRequired._type()

    def is_successful(self):
        return self._type == Successful._type()

    def is_failure(self):
        return self._type == Failure._type()

    def as_not_required(self):
        if self.is_not_required():
            return self
        else:
            return None

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

    def as_one_time_password_required(self):
        if self.is_one_time_password_required():
            return self
        else:
            return None

    def as_secret_code_required(self):
        if self.is_secret_code_required():
            return self
        else:
            return None

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
        return MfaProcess.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == NotRequired._type(): return NotRequired.from_remote_dict(d)
        elif ty == WaitingToStart._type(): return WaitingToStart.from_remote_dict(d);
        elif ty == Starting._type(): return Starting.from_remote_dict(d);
        elif ty == OneTimePasswordRequired._type(): return OneTimePasswordRequired.from_remote_dict(d);
        elif ty == SecretCodeRequired._type(): return SecretCodeRequired.from_remote_dict(d);
        elif ty == Successful._type(): return Successful.from_remote_dict(d);
        elif ty == Failure._type(): return Failure.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'MfaProcess'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == NotRequired._type(): return NotRequired.from_dict(d)
        elif ty == WaitingToStart._type(): return WaitingToStart.from_dict(d);
        elif ty == Starting._type(): return Starting.from_dict(d);
        elif ty == OneTimePasswordRequired._type(): return OneTimePasswordRequired.from_dict(d);
        elif ty == SecretCodeRequired._type(): return SecretCodeRequired.from_dict(d);
        elif ty == Successful._type(): return Successful.from_dict(d);
        elif ty == Failure._type(): return Failure.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'MfaProcess'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class NotRequired(MfaProcess):
    def __init__(self):
        self._type = "NotRequired" 
        super()

    @staticmethod
    def _type(): 
        return "NotRequired"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return NotRequired.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return NotRequired()

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return NotRequired()

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "NotRequired"

class WaitingToStart(MfaProcess):
    def __init__(self, id: str):
        self._type = "WaitingToStart" 
        super()
        self.id = id

    @staticmethod
    def _type(): 
        return "WaitingToStart"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return WaitingToStart.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('id', self.id)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('id', self.id)])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return WaitingToStart(d["id"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return WaitingToStart(d["id"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "WaitingToStart(id=" + self.id + ")"

class Starting(MfaProcess):
    def __init__(self, id: str):
        self._type = "Starting" 
        super()
        self.id = id

    @staticmethod
    def _type(): 
        return "Starting"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Starting.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('id', self.id)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('id', self.id)])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Starting(d["id"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Starting(d["id"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Starting(id=" + self.id + ")"

class OneTimePasswordRequired(MfaProcess):
    def __init__(self,
                 id: str,
                 confirm: MfaProcessConfirm,
                 required_action: LocalizedVariableText,
                 otp: Otp):
        self._type = "OneTimePasswordRequired" 
        super()
        self.id = id
        self.confirm = confirm
        self.required_action = required_action
        self.otp = otp

    @staticmethod
    def _type(): 
        return "OneTimePasswordRequired"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return OneTimePasswordRequired.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('confirm', self.confirm.__to_remote_dict()),
            ('requiredAction', self.required_action.__to_remote_dict()),
            ('otp', self.otp.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('confirm', self.confirm.to_dict()),
            ('required_action', self.required_action.to_dict()),
            ('otp', self.otp.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return OneTimePasswordRequired(d["id"],
                                       MfaProcessConfirm.from_remote_dict(d["confirm"]),
                                       LocalizedVariableText.from_remote_dict(d["requiredAction"]),
                                       Otp.from_remote_dict(d["otp"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return OneTimePasswordRequired(d["id"],
                                       MfaProcessConfirm.from_dict(d["confirm"]),
                                       LocalizedVariableText.from_dict(d["required_action"]),
                                       Otp.from_dict(d["otp"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("OneTimePasswordRequired(id=" + self.id + 
                                        ", confirm=" + repr(self.confirm) + 
                                        ", required_action=" + repr(self.required_action) + 
                                        ", otp=" + repr(self.otp) + ")")

class SecretCodeRequired(MfaProcess):
    def __init__(self,
                 id: str,
                 provider: MoneyAccountProvider,
                 required_action: LocalizedVariableText,
                 expire: Expire):
        self._type = "SecretCodeRequired" 
        super()
        self.id = id
        self.provider = provider
        self.required_action = required_action
        self.expire = expire

    @staticmethod
    def _type(): 
        return "SecretCodeRequired"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return SecretCodeRequired.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('provider', self.provider.__to_remote_dict()),
            ('requiredAction', self.required_action.__to_remote_dict()),
            ('expire', self.expire.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('provider', self.provider.to_dict()),
            ('required_action', self.required_action.to_dict()),
            ('expire', self.expire.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return SecretCodeRequired(d["id"],
                                  MoneyAccountProvider.from_remote_dict(d["provider"]),
                                  LocalizedVariableText.from_remote_dict(d["requiredAction"]),
                                  Expire.from_remote_dict(d["expire"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return SecretCodeRequired(d["id"],
                                  MoneyAccountProvider.from_dict(d["provider"]),
                                  LocalizedVariableText.from_dict(d["required_action"]),
                                  Expire.from_dict(d["expire"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("SecretCodeRequired(id=" + self.id + 
                                   ", provider=" + repr(self.provider) + 
                                   ", required_action=" + repr(self.required_action) + 
                                   ", expire=" + repr(self.expire) + ")")

class Successful(MfaProcess):
    def __init__(self, id: str):
        self._type = "Successful" 
        super()
        self.id = id

    @staticmethod
    def _type(): 
        return "Successful"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Successful.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('id', self.id)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('id', self.id)])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Successful(d["id"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Successful(d["id"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Successful(id=" + self.id + ")"

class Failure(MfaProcess):
    def __init__(self, id: str, reason: LocalizedText):
        self._type = "Failure" 
        super()
        self.id = id
        self.reason = reason

    @staticmethod
    def _type(): 
        return "Failure"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Failure.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('id', self.id),
            ('reason', self.reason.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('id', self.id),
            ('reason', self.reason.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Failure(d["id"],
                       LocalizedText.from_remote_dict(d["reason"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Failure(d["id"],
                       LocalizedText.from_dict(d["reason"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Failure(id=" + self.id + 
                        ", reason=" + repr(self.reason) + ")")