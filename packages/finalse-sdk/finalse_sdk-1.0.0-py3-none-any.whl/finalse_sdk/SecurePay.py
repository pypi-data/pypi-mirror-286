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
from finalse_sdk.QrCode import QrCode
from finalse_sdk.SecurePayPurpose import SecurePayPurpose
from typing import Dict
import json


class SecurePay:
    def __init__(self, purpose: SecurePayPurpose, link: str, qr_code: QrCode):
        self._type = "SecurePay" 
        self.purpose = purpose
        self.link = link
        self.qr_code = qr_code

    @staticmethod
    def _type(): 
        return "SecurePay"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return SecurePay.from_remote_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('purpose', self.purpose.__to_remote_dict()),
            ('link', self.link),
            ('qrCode', self.qr_code.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('purpose', self.purpose.to_dict()),
            ('link', self.link),
            ('qr_code', self.qr_code.to_dict())
        ])

    @staticmethod
    def from_remote_dict(d: Dict[str, any]):
        return SecurePay(SecurePayPurpose.from_remote_dict(d["purpose"]),
                         d["link"],
                         QrCode.from_remote_dict(d["qrCode"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return SecurePay(SecurePayPurpose.from_dict(d["purpose"]),
                         d["link"],
                         QrCode.from_dict(d["qr_code"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("SecurePay(purpose=" + repr(self.purpose) + 
                          ", link=" + self.link + 
                          ", qr_code=" + repr(self.qr_code) + ")")