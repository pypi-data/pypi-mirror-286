from sqlglot import parse_one, exp


class Session():
    def __init__(self, db, params):
        self.database = db
        self.params = params

    def is_type(tree, _type):
        if len(list(tree.find_all(_type))) > 0:
            return True
        return False

    def generateNativeSQL(self, aSql):
        tree = parse_one(aSql)
        if type(tree) != exp.Select:
            raise Exception('As of now, only select statements are supported.', aSql)
        blocked = [exp.DML, exp.DDL, exp.Command, exp.Commit, exp.Drop, exp.TruncateTable]
        for _type in blocked:
            if Session.is_type(tree, _type):
                raise Exception('The SQL contains either DML or DDL', aSql)
        # prepare_table_map
        tbl_map = {}
        for tbl in self.database.tables:
            tbl_map[tbl.pub_name.lower()] = tbl

        print("Input: ", aSql)

        def transformer(node):
            if isinstance(node, exp.Table):
                tbl_name_c = node.this.this
                tbl_name = tbl_name_c.lower()
                if tbl_name not in tbl_map:
                    raise Exception('No such table found.', tbl_name_c)
                mtable = tbl_map[tbl_name]
                msql = mtable.get_alias_sql(self.params)
                return parse_one(msql)
            return node

        new_tree = tree.transform(transformer)
        return new_tree.sql()
