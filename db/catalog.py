class Catalog:
    def __init__(self, storage):
        self.storage = storage
        self.schema = self.storage.read_schema()
        if not isinstance(self.schema, dict):
            print("Warning: Schema was not a dictionary. Resetting.")
            self.schema = {}
    
    def get_table(self, table_name):
        """Get schema for table, or None if doesn't exist"""
        return self.schema.get(table_name)
    
    def table_exists(self, table_name):
        return table_name in self.schema
    
    def list_tables(self):
        """Return list of all table names"""
        return list(self.schema.keys())
    
    def create_table(self, table_name, columns_with_constraints):
        """
        Create a new table with constraints.
        columns_with_constraints: list of (col_name, col_type, constraints)
        constraints: list of strings like ["PRIMARY KEY"] or ["UNIQUE"]
        """
        if table_name in self.schema:
            raise Exception(f"Table '{table_name}' already exists")
        
        # Initialize
        column_defs = {}
        primary_key = None
        unique_columns = []
        column_order = []
        
        # Parse each column
        for col_name, col_type, constraints in columns_with_constraints:
            column_defs[col_name] = col_type.upper()
            column_order.append(col_name)
            
            # Check constraints
            if constraints:
                if "PRIMARY KEY" in constraints:
                    if primary_key is not None:
                        raise Exception("Only one PRIMARY KEY allowed per table")
                    primary_key = col_name
                
                if "UNIQUE" in constraints:
                    unique_columns.append(col_name)
        
        table_schema = {
            "columns": column_defs,
            "primary_key": primary_key,
            "unique_columns": unique_columns,
            "column_order": column_order  # Important for INSERT order
        }
        
        self.schema[table_name] = table_schema
        self.storage.set_table_schema(table_name, table_schema)
        self.storage.write_table(table_name, [])  # Create empty table
        
        return table_schema
    
    def get_table_schema(self, table_name):
        """Get complete schema for a table"""
        return self.schema.get(table_name)
    
    def validate_insert(self, table_name, values):
        """
        Validate values against table schema.
        Returns (is_valid, error_message)
        """
        schema = self.get_table_schema(table_name)
        if not schema:
            return False, f"Table '{table_name}' does not exist"
        
        # Check column count
        expected_count = len(schema["column_order"])
        if len(values) != expected_count:
            return False, f"Expected {expected_count} values, got {len(values)}"
        
        # Check data types (basic check)
        for i, (col_name, value) in enumerate(zip(schema["column_order"], values)):
            col_type = schema["columns"][col_name]
            
            # Basic type checking
            if col_type == "INT":
                if not isinstance(value, int):
                    return False, f"Column '{col_name}' expects INT, got {type(value).__name__}"
            elif col_type == "TEXT":
                if not isinstance(value, str):
                    return False, f"Column '{col_name}' expects TEXT, got {type(value).__name__}"
        
        return True, ""