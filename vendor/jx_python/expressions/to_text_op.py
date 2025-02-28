# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from jx_base.expressions.python_script import PythonScript

from jx_base.expressions import ToTextOp as _ToTextOp
from jx_python.expressions._utils import Python
from mo_json import JX_TEXT


class ToTextOp(_ToTextOp):
    def to_python(self, loop_depth=0):
        missing = self.term.missing(Python).to_python(loop_depth)
        value = self.term.to_python(loop_depth)
        return PythonScript(
            locals=value.locals, loop_depth=loop_depth, type=JX_TEXT, source=value.source, frum=self, miss=missing
        )
