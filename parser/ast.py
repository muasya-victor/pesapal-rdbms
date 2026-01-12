class CreateTable:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns  # list of (name, type, constraints)

class SelectQuery:
    def __init__(self, table_name, columns, where_clause=None):
        self.table_name = table_name
        self.columns = columns  # ["*"] or ["col1", "col2"]
        self.where = where_clause  # (column, operator, value)

class InsertQuery:
    def __init__(self, table_name, values):
        self.table_name = table_name
        self.values = values  # list of values