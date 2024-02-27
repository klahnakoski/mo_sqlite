# encoding: utf-8
# THIS FILE IS AUTOGENERATED!
from setuptools import setup
setup(
    author='Kyle Lahnakoski',
    author_email='kyle@lahnakoski.com',
    classifiers=["Development Status :: 4 - Beta","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules","License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)","Topic :: Database","Topic :: Utilities","Programming Language :: SQL","Programming Language :: Python :: 3.8","Programming Language :: Python :: 3.9","Programming Language :: Python :: 3.11","Programming Language :: Python :: 3.12"],
    description='Multithreading for Sqlite, plus expression composition',
    extras_require={"tests":["mo-testing>=7.523.24033"]},
    include_package_data=True,
    install_requires=["jx-python==4.547.24058","mo-dots==9.547.24058","mo-files==6.547.24058","mo-future==7.546.24057","mo-imports==7.546.24057","mo-json==6.547.24058","mo-kwargs==7.547.24058","mo-logs==8.547.24058","mo-math==7.547.24058","mo-sql==4.547.24058","mo-sql==4.547.24058","mo-threads==6.547.24058","mo-times==5.547.24058"],
    license='MPL 2.0',
    long_description='# More SQLite!\n\nMultithreading for Sqlite, plus expression composition\n\n## Multi-threaded Sqlite\n\nThis module wraps the `sqlite3.connection` with thread-safe traffic manager.  Here is typical usage: \n\n    from mo_sqlite import Sqlite\n    db = Sqlite("mydb.sqlite")\n    with db.transaction() as t:\n        t.command("insert into mytable values (1, 2, 3)")\n\nWhile you may have each thread own a `sqlite3.connection` to the same file, you will still get exceptions when another thread has the file locked.\n\n## Pull JSON out of database\n\nThis module includes a minimum experimental structure that can describe pulling deeply nested JSON documents out of a normalized database.  The tactic is to shape a single query who\'s resultset can be easily converted to the desired JSON by Python. Read more on [pulling json from a database](docs/JSON%20in%20Database.md)\n\nThere are multiple normal forms, including domain key normal form, and columnar form;  these have a multitude one-to-one relations, all represent the same logical schema, but differ in their access patterns to optimize for particular use cases.  This module intends to hide the particular database schema from the caller; exposing just the logical schema. \n\n\n\nThis experiment compliments the [mo-columns](https://github.com/klahnakoski/mo-columns) experiment, which is about pushing JSON into a database. \n   ',
    long_description_content_type='text/markdown',
    name='mo-sqlite',
    packages=["mo_sqlite","mo_sqlite.expressions"],
    url='https://github.com/klahnakoski/mo-sqlite',
    version='2.548.24058'
)