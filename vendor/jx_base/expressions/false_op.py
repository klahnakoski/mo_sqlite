# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#


from jx_base.expressions.literal import Literal
from mo_imports import export, expect
from mo_json.types import JX_BOOLEAN

TRUE = expect("TRUE")


class FalseOp(Literal):
    _jx_type = JX_BOOLEAN

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, op=None, term=None):
        Literal.__init__(self, False)

    @classmethod
    def define(cls, expr):
        return FALSE

    def __nonzero__(self):
        return False

    def __eq__(self, other):
        return (other is FALSE) or (other is False)

    def __data__(self):
        return False

    def vars(self):
        return set()

    def map(self, map_):
        return self

    def missing(self, lang):
        return FALSE

    def invert(self, lang):
        return TRUE

    @property
    def jx_type(self):
        return JX_BOOLEAN

    def __call__(self, row=None, rownum=None, rows=None):
        return False

    def __str__(self):
        return "false"

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False


FALSE = FalseOp()

export("jx_base.expressions._utils", FALSE)
export("jx_base.expressions.expression", FALSE)
export("jx_base.expressions.literal", FALSE)
