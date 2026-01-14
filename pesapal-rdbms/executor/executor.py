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
    
    # executor/join_executor.py

class JoinExecutor:
    @staticmethod
    def nested_loop_join(left_rows, right_rows, left_key_idx, right_key_idx):
        """
        Perform nested loop join (naive but works).
        Returns list of joined rows.
        """
        results = []
        
        for left_row in left_rows:
            left_key = left_row[left_key_idx]
            
            for right_row in right_rows:
                right_key = right_row[right_key_idx]
                
                if left_key == right_key:
                    # Merge rows (all columns from both tables)
                    joined_row = left_row + right_row
                    results.append(joined_row)
        
        return results
    
    @staticmethod
    def parse_column_reference(col_ref, table_aliases, catalog):
        """
        Parse column reference like 'users.id' or 'u.id'
        Returns: (table_name, column_name)
        """
        if '.' in col_ref:
            table_ref, column_name = col_ref.split('.')
            
            # Find actual table name from alias
            for table, alias in table_aliases.items():
                if table_ref == table or table_ref == alias:
                    return table, column_name
            
            raise Exception(f"Unknown table or alias: {table_ref}")
        else:
            # Simple column name - need to figure out which table
            # For simplicity in demo, we'll require table prefix
            raise Exception(f"Column reference must include table: {col_ref}")
    
    @staticmethod
    def execute_join(table_info, catalog, storage):
        """
        Execute a JOIN query.
        Returns: (joined_rows, combined_schema)
        """
        if table_info['type'] != 'join':
            raise Exception("Not a JOIN query")
        
        tables = table_info['tables']
        aliases = table_info['aliases']
        left_cond, right_cond = table_info['join_condition']
        
        # Parse join conditions
        left_table, left_col = JoinExecutor.parse_column_reference(left_cond, aliases, catalog)
        right_table, right_col = JoinExecutor.parse_column_reference(right_cond, aliases, catalog)
        
        # Read both tables
        left_rows = storage.read_table(left_table)
        right_rows = storage.read_table(right_table)
        
        # Get schemas to find column indices
        left_schema = catalog.get_table_schema(left_table)
        right_schema = catalog.get_table_schema(right_table)
        
        if not left_schema or not right_schema:
            raise Exception(f"Table not found: {left_table} or {right_table}")
        
        # Find column indices for join keys
        left_key_idx = left_schema["column_order"].index(left_col)
        right_key_idx = right_schema["column_order"].index(right_col)
        
        # Perform join
        joined_rows = JoinExecutor.nested_loop_join(
            left_rows, right_rows, left_key_idx, right_key_idx
        )
        
        # Create combined schema for result
        combined_schema = {
            'columns': {**left_schema['columns'], **right_schema['columns']},
            'column_order': left_schema['column_order'] + right_schema['column_order'],
            'table_aliases': aliases
        }
        
        return joined_rows, combined_schema