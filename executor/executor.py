class Executor:
    def __init__(self, catalog, storage):
        self.catalog = catalog
        self.storage = storage
    
    def execute_create_table(self, create_ast):
        # Create table with constraints
        pass
    
    def execute_insert(self, insert_ast):
        # Validate and insert
        pass
    
    def execute_select(self, select_ast):
        # Read table, apply WHERE, return rows
        pass