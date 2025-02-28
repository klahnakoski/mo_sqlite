# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from mo_imports import export

from jx_base.expressions import WhenOp as _WhenOp
from jx_base.expressions.python_script import PythonScript
from jx_python.utils import merge_locals


class WhenOp(_WhenOp):
    def to_python(self, loop_depth=0):
        when = self.when.to_python(loop_depth)
        then = self.then.to_python(loop_depth)
        els_ = self.els_.to_python(loop_depth)
        return PythonScript(
            merge_locals(when.locals, then.locals, els_.locals),
            loop_depth,
            then.jx_type | els_.jx_type,
            f"({then.source}) if ({when.source}) else ({els_.source})",
            self,
        )


export("jx_python.expressions._utils", WhenOp)
