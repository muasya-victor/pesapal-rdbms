class Catalog:
    def __init__(self, storage):
        self.storage = storage
        self.schema = self.storage.read_schema()
        if not isinstance(self.schema, dict):
            print("Warning: Schema was not a dictionary. Resetting.")
            self.schema = {}
    
    def create_table(self, table_name, columns):
        """
        Create a new table.
        columns: list of tuples (column_name, column_type)
        Example: [("id", "INT"), ("name", "TEXT")]
        """
        if table_name in self.schema:
            raise Exception(f"Table '{table_name}' already exists")
        
        table_schema = {
            "columns": {col_name: col_type for col_name, col_type in columns},
            "primary_key": None,  # We'll add later
            "unique": []          # We'll add later
        }
        
        self.schema[table_name] = table_schema
        self.storage.set_table_schema(table_name, table_schema)
        
        # Initialize empty table file
        self.storage.write_table(table_name, [])
        
        return table_schema
    
    def get_table(self, table_name):
        """Get schema for table, or None if doesn't exist"""
        return self.schema.get(table_name)
    
    def table_exists(self, table_name):
        return table_name in self.schema
    
    def list_tables(self):
        """Return list of all table names"""
        return list(self.schema.keys())