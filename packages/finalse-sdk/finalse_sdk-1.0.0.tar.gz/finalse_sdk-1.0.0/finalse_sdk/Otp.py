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
from finalse_sdk.Expire import Expire
from finalse_sdk.OtpAction import OtpAction
from finalse_sdk.OtpChannel import OtpChannel
from typing import Dict
from typing import Optional
import json


class Otp:
    def __init__(self,
                 expire: Expire,
                 nb_verify_attempts: int,
                 prefix: Optional[str],
                 channel: OtpChannel,
                 action: OtpAction):
        self._type = "Otp" 
        self.expire = expire
        self.nb_verify_attempts = nb_verify_attempts
        self.prefix = prefix
        self.channel = channel
        self.action = action

    @staticmethod
    def _type(): 
        return "Otp"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Otp.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('expire', self.expire.__to_remote_dict()),
            ('nbVerifyAttempts', self.nb_verify_attempts),
            ('prefix', self.prefix),
            ('channel', self.channel.__to_remote_dict()),
            ('action', self.action.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('expire', self.expire.to_dict()),
            ('nb_verify_attempts', self.nb_verify_attempts),
            ('prefix', self.prefix),
            ('channel', self.channel.to_dict()),
            ('action', self.action.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return Otp(Expire.from_remote_dict(d["expire"]),
                   d["nbVerifyAttempts"],
                   d["prefix"] if "prefix" in d else None,
                   OtpChannel.from_remote_dict(d["channel"]),
                   OtpAction.from_remote_dict(d["action"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Otp(Expire.from_dict(d["expire"]),
                   d["nb_verify_attempts"],
                   d["prefix"] if "prefix" in d else None,
                   OtpChannel.from_dict(d["channel"]),
                   OtpAction.from_dict(d["action"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Otp(expire=" + repr(self.expire) + 
                    ", nb_verify_attempts=" + str(self.nb_verify_attempts) + 
                    ", prefix=" + str(self.prefix) + 
                    ", channel=" + repr(self.channel) + 
                    ", action=" + repr(self.action) + ")")