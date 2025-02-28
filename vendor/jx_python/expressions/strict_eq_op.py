# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#


from jx_base.expressions import StrictEqOp as _StrictEqOp, FALSE
from jx_base.expressions.python_script import PythonScript
from jx_python.utils import merge_locals
from mo_json import JX_BOOLEAN


class StrictEqOp(_StrictEqOp):
    def to_python(self, loop_depth=0):
        lhs = self.lhs.to_python(loop_depth)
        rhs = self.rhs.to_python(loop_depth)
        return PythonScript(
            merge_locals(lhs.locals, rhs.locals),
            loop_depth,
            JX_BOOLEAN,
            "(" + lhs.source + ") == (" + rhs.source + ")",
            FALSE,
        )
