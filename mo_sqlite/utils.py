# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#
import re
from collections import Mapping, namedtuple

from mo_dots import coalesce, listwrap, to_data
from mo_logs import logger
from mo_logs.strings import quote
from mo_sql import *
from mo_times import Date, Duration


TYPE_CHECK = True

FORMAT_COMMAND = 'Running command from "{{file}}:{{line}}"\n{{command|limit(1000)|indent}}'


CommandItem = namedtuple("CommandItem", ("command", "result", "is_done", "trace", "transaction"))

_simple_word = re.compile(r"^[_a-zA-Z][_0-9a-zA-Z]*$", re.UNICODE)


def _simple_quote_column(name):
    if _simple_word.match(name):
        return name
    return quote(name)


def quote_column(*path):
    if TYPE_CHECK:
        if not path:
            logger.error("expecting a name")
        for p in path:
            if not is_text(p):
                logger.error("expecting strings, not {type}", type=p.__class__.__name__)
    try:
        output = ConcatSQL(SQL_SPACE, JoinSQL(SQL_DOT, [SQL(_simple_quote_column(p)) for p in path]), SQL_SPACE,)
        return output
    except Exception as e:
        logger.error("Not expacted", cause=e)


def sql_alias(value, alias):
    if not isinstance(value, SQL) or not is_text(alias):
        logger.error("Expecting (SQL, text) parameters")
    return ConcatSQL(value, SQL_AS, quote_column(alias))


def sql_call(func_name, *parameters):
    return ConcatSQL(SQL(func_name), sql_iso(JoinSQL(SQL_COMMA, parameters)))


def quote_value(value):
    if isinstance(value, (Mapping, list)):
        return SQL(".")
    elif isinstance(value, Date):
        return SQL(str(value.unix))
    elif isinstance(value, Duration):
        return SQL(str(value.seconds))
    elif is_text(value):
        return SQL("'" + value.replace("'", "''") + "'")
    elif value == None:
        return SQL_NULL
    elif value is True:
        return SQL_TRUE
    elif value is False:
        return SQL_FALSE
    else:
        return SQL(str(value))


def quote_list(values):
    return sql_iso(sql_list(map(quote_value, values)))


def sql_eq(**item):
    """
    RETURN SQL FOR COMPARING VARIABLES TO VALUES (AND'ED TOGETHER)

    :param item: keyword parameters representing variable and value
    :return: SQL
    """
    return SQL_AND.join([
        ConcatSQL(quote_column(str(k)), SQL_EQ, quote_value(v))
        if v != None
        else ConcatSQL(quote_column(str(k)), SQL_IS_NULL)
        for k, v in item.items()
    ])


def sql_lt(**item):
    """
    RETURN SQL FOR LESS-THAN (<) COMPARISON BETWEEN VARIABLES TO VALUES

    :param item: keyword parameters representing variable and value
    :return: SQL
    """
    k, v = first(item.items())
    return ConcatSQL(quote_column(k), SQL_LT, quote_value(v))


def sql_query(command):
    """
    VERY BASIC QUERY EXPRESSION TO SQL
    :param command: jx-expression
    :return: SQL
    """
    command = to_data(command)
    acc = [SQL_SELECT]
    if command.select:
        acc.append(JoinSQL(SQL_COMMA, map(quote_column, listwrap(command.select))))
    else:
        acc.append(SQL_STAR)

    acc.append(SQL_FROM)
    acc.append(quote_column(command["from"]))
    if command.where:
        acc.append(SQL_WHERE)
        if command.where.eq:
            acc.append(sql_eq(**command.where.eq))
        else:
            from mo_sqlite.expressions import SQLang
            from jx_base import jx_expression

            where = jx_expression(command.where).partial_eval(SQLang).to_sql[0].b
            acc.append(where)

    sort = coalesce(command.orderby, command.sort)
    if sort:
        acc.append(SQL_ORDERBY)
        acc.append(JoinSQL(SQL_COMMA, map(quote_column, listwrap(sort))))

    if command.limit:
        acc.append(SQL_LIMIT)
        acc.append(JoinSQL(SQL_COMMA, map(quote_value, listwrap(command.limit))))

    return ConcatSQL(*acc)


def sql_create(table, properties, primary_key=None, unique=None):
    """
    :param table:  NAME OF THE TABLE TO CREATE
    :param properties: DICT WITH {name: type} PAIRS (type can be plain text)
    :param primary_key: COLUMNS THAT MAKE UP THE PRIMARY KEY
    :param unique: COLUMNS THAT SHOULD BE UNIQUE
    :return:
    """
    acc = [
        SQL_CREATE,
        quote_column(table),
        SQL_OP,
        sql_list([quote_column(k) + SQL(v) for k, v in properties.items()]),
    ]
    primary_key = listwrap(primary_key)

    if primary_key:
        acc.append(SQL_COMMA),
        acc.append(SQL(" PRIMARY KEY ")),
        acc.append(sql_iso(sql_list([quote_column(c) for c in listwrap(primary_key)])))
    if unique:
        acc.append(SQL_COMMA),
        acc.append(SQL(" UNIQUE ")),
        acc.append(sql_iso(sql_list([quote_column(c) for c in listwrap(unique)])))

    acc.append(SQL_CP)
    if primary_key and not (len(primary_key) == 1 and properties[primary_key[0]] == "INTEGER"):
        acc.append(SQL(" WITHOUT ROWID"))
    return ConcatSQL(*acc)


def sql_insert(table, records):
    records = listwrap(records)
    keys = list({k for r in records for k in r.keys()})
    return ConcatSQL(
        SQL_INSERT,
        quote_column(table),
        sql_iso(sql_list(map(quote_column, keys))),
        SQL_VALUES,
        sql_list(sql_iso(sql_list([quote_value(r[k]) for k in keys])) for r in records),
    )


BEGIN = "BEGIN"
COMMIT = "COMMIT"
ROLLBACK = "ROLLBACK"
