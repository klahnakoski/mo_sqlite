# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#


from jx_base.expressions import FloorOp as _FloorOp
from jx_base.expressions.python_script import PythonScript


class FloorOp(_FloorOp):
    def to_python(self, loop_depth=0):
        return PythonScript(
            {},
            loop_depth,
            ("mo_math.floor(" + (self.lhs).to_python(loop_depth) + ", " + (self.rhs).to_python(loop_depth) + ")"),
        )
