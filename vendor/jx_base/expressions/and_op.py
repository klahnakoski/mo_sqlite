# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#


from jx_base.expressions.base_multi_op import BaseMultiOp
from jx_base.expressions.false_op import FALSE
from jx_base.expressions.true_op import TRUE
from jx_base.language import is_op
from mo_imports import expect, export
from mo_json.types import JX_BOOLEAN

NotOp, OrOp, ToBooleanOp = expect("NotOp", "OrOp", "ToBooleanOp")


class AndOp(BaseMultiOp):
    _jx_type = JX_BOOLEAN

    def __init__(self, *terms, nulls=True):
        BaseMultiOp.__init__(self, *terms, nulls=nulls)

    def __data__(self):
        return {"and": [t.__data__() for t in self.terms]}

    def __call__(self, row, rownum=None, rows=None):
        for a in self.terms:
            if not a(row, rownum, rows):
                return False
        return True

    def missing(self, lang):
        if self.decisive:
            return FALSE
        return OrOp(*(t.missing(lang) for t in self.terms))

    def invert(self, lang):
        return OrOp(*(t.invert(lang) for t in self.terms)).partial_eval(lang)

    def partial_eval(self, lang):
        # MERGE IDENTICAL NESTED QUERIES
        # NEST DEEP NESTED QUERIES
        or_terms = [[]]  # LIST OF TUPLES FOR or-ing and and-ing
        for i, t in enumerate(self.terms):
            simple = ToBooleanOp(t).partial_eval(lang)
            if simple is TRUE:
                continue
            elif simple is FALSE:
                return FALSE
            elif is_op(simple, AndOp):
                for and_terms in or_terms:
                    for tt in simple.terms:
                        if tt in and_terms:
                            continue
                        if (NotOp(tt)).partial_eval(lang) in and_terms:
                            or_terms.remove(and_terms)
                            break
                        and_terms.append(tt)
                continue
            elif is_op(simple, OrOp):
                or_terms = [
                    and_terms + ([o] if o not in and_terms else [])
                    for o in simple.terms
                    for and_terms in or_terms
                    if NotOp(o).partial_eval(lang) not in and_terms
                ]
                continue
            for and_terms in list(or_terms):
                inv = lang.NotOp(simple).partial_eval(lang)
                if inv in and_terms:
                    or_terms.remove(and_terms)
                elif simple not in and_terms:
                    and_terms.append(simple)
        if len(or_terms) == 0:
            return FALSE
        elif len(or_terms) == 1:
            and_terms = or_terms[0]
            if len(and_terms) == 0:
                return TRUE
            elif len(and_terms) == 1:
                return and_terms[0]
            else:
                return lang.AndOp(*and_terms, nulls=self.decisive)

        return OrOp(
            *(lang.AndOp(*and_terms) if len(and_terms) > 1 else and_terms[0] for and_terms in or_terms)
        ).partial_eval(lang)


export("jx_base.expressions.expression", AndOp)
export("jx_base.expressions.base_multi_op", AndOp)
