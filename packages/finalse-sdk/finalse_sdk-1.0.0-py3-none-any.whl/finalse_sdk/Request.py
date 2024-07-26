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

import time

class Request:

    def __init__(self, signed_headers, method, path, query_string, body_hash):
        self.nonce = int(round(time.time() * 1000))
        self.signed_headers = signed_headers
        self.method = method
        self.path = path
        self.query_string = query_string
        self.body_hash = body_hash

    def to_message(self):
        return (
                str(self.nonce) +
                "".join([name + ":" + value for name, value in list(self.signed_headers.items()) ]) +
                self.method +
                self.path +
                (self.query_string if self.query_string is not None else "") +
                (self.body_hash if self.body_hash is not None else "")
        )