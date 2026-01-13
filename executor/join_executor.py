# executor/join_executor.py
class JoinExecutor:
    def __init__(self):
        pass
    
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
            raise Exception(f"Column reference must include table: {col_ref}")
    
    def execute_join(self, table_info, catalog, storage):
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
        left_table, left_col = self.parse_column_reference(left_cond, aliases, catalog)
        right_table, right_col = self.parse_column_reference(right_cond, aliases, catalog)
        
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
        joined_rows = self.nested_loop_join(
            left_rows, right_rows, left_key_idx, right_key_idx
        )
        
        # Create combined schema with proper column names
        # Prefix columns with table names to avoid conflicts
        combined_columns = {}
        combined_column_order = []
        
        # Add left table columns with prefixes
        for col in left_schema["column_order"]:
            prefixed_col = f"{left_table}.{col}"
            combined_columns[prefixed_col] = left_schema["columns"][col]
            combined_column_order.append(prefixed_col)
        
        # Add right table columns with prefixes  
        for col in right_schema["column_order"]:
            prefixed_col = f"{right_table}.{col}"
            combined_columns[prefixed_col] = right_schema["columns"][col]
            combined_column_order.append(prefixed_col)
        
        combined_schema = {
            'columns': combined_columns,
            'column_order': combined_column_order,
            'table_aliases': aliases,
            'table_mapping': {
                left_table: list(range(len(left_schema["column_order"]))),
                right_table: list(range(len(left_schema["column_order"]), 
                                      len(left_schema["column_order"]) + len(right_schema["column_order"])))
            }
        }
        
        return joined_rows, combined_schema