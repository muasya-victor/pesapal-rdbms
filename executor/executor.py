class Executor:
    def __init__(self, catalog, storage):
        self.catalog = catalog
        self.storage = storage
    
    def execute_create_table(self, table_name, columns):
        """Execute CREATE TABLE command"""
        return self.catalog.create_table(table_name, columns)
    
    def execute_insert(self, table_name, values):
        """Execute INSERT command with validation"""
        # First validate
        valid, error = self.catalog.validate_insert(table_name, values)
        if not valid:
            raise Exception(f"Insert validation failed: {error}")
        
        # Check constraints (will be enhanced later)
        self._check_constraints(table_name, values)
        
        # Insert the row
        rows = self.storage.read_table(table_name)
        rows.append(values)
        self.storage.write_table(table_name, rows)
        
        return 1  # Number of rows inserted
    
    def _check_constraints(self, table_name, values):
        """Basic constraint checking (will be enhanced in Step 4)"""
        schema = self.catalog.get_table_schema(table_name)
        if not schema:
            raise Exception(f"Table '{table_name}' not found")
        
        # For now, just a placeholder
        # We'll implement full constraint checking in next step
        pass
    
    def execute_select(self, table_name, columns=None, where=None):
        """Execute SELECT command"""
        rows = self.storage.read_table(table_name)
        
        # If WHERE clause provided, filter rows
        if where:
            column_name, operator, value = where
            # For now, only support equality
            if operator == '=':
                schema = self.catalog.get_table_schema(table_name)
                col_index = schema["column_order"].index(column_name)
                rows = [row for row in rows if row[col_index] == value]
        
        # If specific columns requested, filter columns
        if columns and columns != ['*']:
            schema = self.catalog.get_table_schema(table_name)
            result = []
            for row in rows:
                filtered_row = []
                for col in columns:
                    col_index = schema["column_order"].index(col)
                    filtered_row.append(row[col_index])
                result.append(filtered_row)
            rows = result
        
        return rows