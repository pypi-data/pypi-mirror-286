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


class OtpChannel(ABC):
    def is_sms_channel(self):
        return self._type == SmsChannel._type()

    def is_email_channel(self):
        return self._type == EmailChannel._type()

    def as_sms_channel(self):
        if self.is_sms_channel():
            return self
        else:
            return None

    def as_email_channel(self):
        if self.is_email_channel():
            return self
        else:
            return None

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return OtpChannel.from_remote_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == SmsChannel._type(): return SmsChannel.from_remote_dict(d)
        elif ty == EmailChannel._type(): return EmailChannel.from_remote_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'OtpChannel'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == SmsChannel._type(): return SmsChannel.from_dict(d)
        elif ty == EmailChannel._type(): return EmailChannel.from_dict(d);
        else: raise ValueError("Invalid dict submitted for creating 'OtpChannel'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class SmsChannel(OtpChannel):
    def __init__(self, value: str):
        self._type = "SmsChannel" 
        super()
        self.value = value

    @staticmethod
    def _type(): 
        return "SmsChannel"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return SmsChannel.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('value', self.value)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('value', self.value)])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return SmsChannel(d["value"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return SmsChannel(d["value"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "SmsChannel(value=" + self.value + ")"

class EmailChannel(OtpChannel):
    def __init__(self, value: str):
        self._type = "EmailChannel" 
        super()
        self.value = value

    @staticmethod
    def _type(): 
        return "EmailChannel"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return EmailChannel.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [('value', self.value)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('value', self.value)])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return EmailChannel(d["value"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return EmailChannel(d["value"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "EmailChannel(value=" + self.value + ")"