import requests
import json
from config import Config

class MiniDBClient:
    """Wrapper for MiniDB REST API"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or Config.MINIDB_URL
        
    def execute_query(self, sql_command):
        """Execute SQL command via MiniDB API"""
        try:
            response = requests.post(
                f"{self.base_url}/query",
                json={"command": sql_command},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to MiniDB. Make sure it's running on port 2500.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Database error: {str(e)}")
    
    def execute_and_get_results(self, sql_command):
        """Execute query and return parsed results"""
        result = self.execute_query(sql_command)
        
        # Parse MiniDB output format
        if 'error' in result:
            raise Exception(result['error'])
        
        # Extract rows from MiniDB's output format
        output = result.get('result', '')
        lines = output.strip().split('\n')
        
        # Parse rows (skip empty lines and count line)
        rows = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('(') and 'row' in line:
                continue
            if line.startswith('[') and line.endswith(']'):
                # Parse row like: ["value1", "value2"]
                try:
                    # Remove brackets and parse
                    content = line[1:-1]
                    values = []
                    current = ''
                    in_quotes = False
                    quote_char = None
                    
                    for char in content:
                        if char in ('"', "'") and (not current or current[-1] != '\\'):
                            if not in_quotes:
                                in_quotes = True
                                quote_char = char
                            elif char == quote_char:
                                in_quotes = False
                            current += char
                        elif char == ',' and not in_quotes:
                            values.append(self._parse_value(current.strip()))
                            current = ''
                        else:
                            current += char
                    
                    if current:
                        values.append(self._parse_value(current.strip()))
                    
                    rows.append(values)
                except:
                    # If parsing fails, return raw output
                    pass
        
        return rows
    
    def _parse_value(self, value_str):
        """Parse value from string representation"""
        if not value_str:
            return None
        
        # Remove quotes
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        
        # Try to parse as number
        try:
            if '.' in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            return value_str
    
    def table_exists(self, table_name):
        """Check if table exists"""
        try:
            result = self.execute_query(f"SHOW TABLES;")
            output = result.get('result', '')
            return table_name in output
        except:
            return False
    
    def initialize_database(self):
        """Create necessary tables if they don't exist"""
        from config import Config
        
        for table_name, create_sql in Config.TABLES.items():
            if not self.table_exists(table_name):
                print(f"Creating table: {table_name}")
                self.execute_query(create_sql)
    
    # Convenience methods
    def insert(self, table, data):
        """Insert data into table"""
        columns = ', '.join(data.keys())
        values = ', '.join([self._format_value(v) for v in data.values()])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values});"
        return self.execute_query(sql)
    
    def select(self, table, where=None, columns='*'):
        """Select from table"""
        sql = f"SELECT {columns} FROM {table}"
        if where:
            sql += f" WHERE {where}"
        sql += ";"
        return self.execute_and_get_results(sql)
    
    def update(self, table, data, where):
        """Update table"""
        set_clause = ', '.join([f"{k} = {self._format_value(v)}" for k, v in data.items()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where};"
        return self.execute_query(sql)
    
    def delete(self, table, where):
        """Delete from table"""
        sql = f"DELETE FROM {table} WHERE {where};"
        return self.execute_query(sql)
    
    def _format_value(self, value):
        """Format value for SQL"""
        if value is None:
            return 'NULL'
        elif isinstance(value, str):
            return f"'{value.replace("'", "''")}'"
        elif isinstance(value, bool):
            return '1' if value else '0'
        else:
            return str(value)