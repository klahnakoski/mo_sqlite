# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#


from jx_base.expressions import SplitOp as _SplitOp
from jx_base.expressions.python_script import PythonScript


class SplitOp(_SplitOp):
    def to_python(self, loop_depth=0):
        return PythonScript(
            {},
            loop_depth,
            ("(" + (self.value).to_python(loop_depth) + ").split(" + (self.find).to_python(loop_depth) + ")"),
        )
