
# export PYTHONPATH=../src/
# python insert_test.py

import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy import text

from sqlshield.models import *
from sqlshield.shield import *

def loadDb():
    engine = sqlalchemy.create_engine('sqlite:///chinook.db')
    inspector = inspect(engine)

    # Load default DB
    return MDatabase.from_inspector(inspector)

def build_protection(mDb):
    mDb.keep_only_tables(set(['Customer', 'Employee', 'Invoice', 'InvoiceLine']))
    
    tables = mDb.get_table_dict()
    print("Tables: ", tables)
    customer_table = tables['Customer']

    # Change Name of table
    customer_table.pub_name = 'Customers'

    # Add a filter
    customer_table.filters = 'where company = {company}'

    # Drop some colums
    customer_table.drop_columns(set(['Address']))

if __name__ == "__main__":
    mDb = loadDb()
    build_protection(mDb)
    # Column renaming
    d = {'company':'\'Telus\''}
    sess = Session(mDb, d)
    sqls = [
            'drop table t1;'
            'insert into Customers Values(1,2)',
            'create table t (age int)',
            "GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost'; ",
            # "REVOKE SELECT, UPDATE ON MY_TABLE FROM USER1, USER2;",
            "COMMIT;",
            'select * from Employee;drop table Employee;',
            'select * from cusTomers',
            'select * from cusTomer',
        ]
    for sql in sqls:
        try:
            gSQL = sess.generateNativeSQL(sql)
            # GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost'; 
            print("Native SQL: ", gSQL)
        except Exception as e:
            print("ERROR: ", e.args)

