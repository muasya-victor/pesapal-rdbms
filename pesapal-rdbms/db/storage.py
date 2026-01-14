import json
import os
from pathlib import Path

class Storage:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def table_path(self, table_name):
        """Get path for table data file"""
        return self.data_dir / f"{table_name}.json"
    
    def read_table(self, table_name):
        """Read all rows from a table"""
        path = self.table_path(table_name)
        if not path.exists():
            return []  
        with open(path, 'r') as f:
            return json.load(f).get("rows", [])
    
    def write_table(self, table_name, rows):
        """Write rows to table file"""
        path = self.table_path(table_name)
        data = {"rows": rows}
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def table_exists(self, table_name):
        """Check if table file exists"""
        return self.table_path(table_name).exists()
    
    def read_table(self, table_name):
        """Read all rows from a table"""
        path = self.table_path(table_name)
        
        # If file doesn't exist, table is empty
        if not path.exists():
            return []
        
        # If file exists but is empty, table is empty
        if path.stat().st_size == 0:
            return []
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return data.get("rows", [])
        except json.JSONDecodeError:
            print(f"Warning: {table_name}.json contains invalid JSON. Returning empty table.")
            return []
        
    def write_schema(self, schema):
        """Write entire schema catalog"""
        schema_path = self.data_dir / "schema.json"
        schema_path.parent.mkdir(exist_ok=True, parents=True)
        with open(schema_path, 'w') as f:
            json.dump(schema, f, indent=2)
    
    def get_table_schema(self, table_name):
        """Get schema for specific table"""
        schema = self.read_schema()
        return schema.get(table_name)
    
    def set_table_schema(self, table_name, table_schema):
        """Update schema for specific table"""
        schema = self.read_schema()
        schema[table_name] = table_schema
        self.write_schema(schema)

    def read_schema(self):
        """Read entire schema catalog from disk"""
        schema_path = self.data_dir / "schema.json"
        if not schema_path.exists():
            return {}
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        
    def insert_with_index(self, catalog, table_name, values, row_position):
        """Insert a row and update indexes"""
        schema = catalog.get_table_schema(table_name)
        
        # Update primary key index
        if schema.get("primary_key"):
            pk_col = schema["primary_key"]
            pk_index = pk_col  # Get column name
            col_index = schema["column_order"].index(pk_col)
            pk_value = values[col_index]
            
            # Update index
            index = catalog.get_index(table_name, pk_col)
            if index:
                index.add(pk_value, row_position)
        
        # Update unique indexes
        for unique_col in schema.get("unique_columns", []):
            col_index = schema["column_order"].index(unique_col)
            col_value = values[col_index]
            
            index = catalog.get_index(table_name, unique_col)
            if index:
                index.add(col_value, row_position)