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
    
    def read_schema(self):
        """Read entire schema catalog"""
        schema_path = self.data_dir / "schema.json"
        if not schema_path.exists():
            return {}
        with open(schema_path, 'r') as f:
            return json.load(f)
        
    def write_schema(self, schema):
        """Write entire schema catalog"""
        schema_path = self.data_dir / "schema.json"
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