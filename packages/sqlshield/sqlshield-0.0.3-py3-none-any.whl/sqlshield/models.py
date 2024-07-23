# Should extend sqlalchemy.sql.schema.Column
class Column():
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.type = kwargs['type']
        self.primary_key = kwargs.get('primary_key', '')
        self.nullable = kwargs['nullable']
        self.desc = kwargs.get('desc', '')
        self.foreign_keys = []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, __value: object) -> bool:
        _s = self
        _v = __value
        return (_s.name, _s.type, _s.primary_key, _s.desc) == (_v.name, _v.type, _v.primary_key, _v.desc)


class MColumn(Column):
    def __init__(self, pub_name=None, **kwargs):
        super().__init__(**kwargs)
        if pub_name is None:
            pub_name = self.name
        self.pub_name = pub_name

    def generate_schema(self):
        return '[%s] %s' % (self.pub_name, str(self.type))


class Table:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        # self.pk = pk
        self.columns = set()
        self.desc = kwargs['desc']

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, __value: object) -> bool:
        _s = self
        _v = __value
        return (_s.name, _s.pk, _s.columns, _s.desc) == (_v.name, _v.pk, _v.columns, _v.desc)


class MTable(Table):
    def __init__(self, name, desc='', pub_name=None, filters=None):
        super().__init__(name=name, desc=desc)
        if pub_name is None:
            pub_name = self.name
        self.pub_name = pub_name
        self.filters = filters  # template/Format string containing {var1}

    def _get_projections_sql(self):
        result = []
        for col in self.columns:
            result.append("%s as %s" % (col.name, col.pub_name))
        return ', '.join(result)

    def get_alias_sql(self, params):
        filterSQL = ''
        if self.filters:
            filterSQL = self.filters.format(**params)
        sql_template = '(select %s from %s %s) as %s'
        colsql = self._get_projections_sql()
        query = sql_template % (colsql, self.name, filterSQL, self.pub_name)
        return query

    def generate_schema(self):
        cols_info_arr = []
        for col in self.columns:
            cols_info_arr.append(col.generate_schema())
        col_info = ',\n\t'.join(cols_info_arr)
        sql_template = 'CREATE TABLE [%s](\n\t%s\n\t);' % (self.pub_name, col_info)
        return sql_template

    def drop_columns(self, col_names_set):
        to_drop = set()
        for col in self.columns:
            if col.name in col_names_set:
                to_drop.add(col)
        self.columns = self.columns.difference(to_drop)


class MDatabase():
    def __init__(self):
        self.tables = set()
        # self.allowed_commands = ['show databases']
        # self.allowed_all_tables = []

    def generate_schema(self):
        schema_arr = []
        for table in self.tables:
            schema_arr.append(table.generate_schema())
        return '\n'.join(schema_arr)

    def from_inspector(inspector):
        mdb = MDatabase()
        schemas = inspector.get_schema_names()
        for schema in schemas[:1]:
            for table_name in inspector.get_table_names(schema=schema):
                mtable = MTable(table_name)
                mdb.tables.add(mtable)
                for col in inspector.get_columns(table_name, schema=schema):
                    mc = MColumn(**col)
                    mtable.columns.add(mc)
        return mdb

    def get_table_dict(self):
        d = {}
        for tbl in self.tables:
            d[tbl.name] = tbl
        return d

    def keep_only_tables(self, keep_tbls):
        new_tables = set()
        for tbl in self.tables:
            if tbl.name in keep_tbls:
                new_tables.add(tbl)
        self.tables = new_tables

# Database is a collection of Mtables
# Database supports a method like get filter columns.

# Data Type is enum: int, string, boolean
# A filter is an equality between column and a parameter
