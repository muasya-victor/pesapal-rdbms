from db.storage import Storage
from db.catalog import Catalog
from parser.tokenizer import tokenize
from executor.executor import Executor
from parser.parser import Parser

class MiniDBShell:
    def __init__(self):
        self.running = True
        self.storage = Storage()
        self.catalog = Catalog(self.storage)
        # self.executor = Executor(self.catalog, self.storage)
        self.parser = Parser()
    
    def run(self):
        print("Welcome To Shell - Type 'EXIT;' to quit")
        while self.running:
            try:
                command = input("muasya-rdbms> ").strip()
                if not command:
                    continue
                self.handle_command(command)
            except KeyboardInterrupt:
                print("\nUse EXIT; to quit")
            except EOFError:
                break

    def get_full_command(self):
        """Collect lines until semicolon"""
        lines = []
        while True:
            line = input("... " if lines else "mini-db> ")
            lines.append(line)
            if ';' in line:
                break
        return ' '.join(lines)
    
    def handle_command(self, command):
        cmd = command.rstrip(';').strip()
        
        # Exit command
        if cmd.upper() in ['EXIT', 'QUIT']:
            print("Goodbye!")
            self.running = False
            return
        
        # CREATE TABLE command
        if cmd.upper().startswith("CREATE TABLE"):
            try:
                table_name, columns = self.parser.parse_create_table(cmd)
                self.catalog.create_table(table_name, columns)
                print(f"Table '{table_name}' created successfully")
            except Exception as e:
                print(f"Error: {e}")
            return
        
        # SHOW TABLES command
        if cmd.upper() == "SHOW TABLES":
            tables = self.catalog.list_tables()
            if tables:
                print("\n".join(tables))
            else:
                print("No tables exist")
            return
        
        # INSERT command - USING PARSER
        if cmd.upper().startswith("INSERT INTO"):
            try:
                # Parse the INSERT command
                table_name, values = self.parser.parse_insert(cmd)
                
                # 1. Validate against schema
                valid, error_msg = self.catalog.validate_insert(table_name, values)
                if not valid:
                    raise Exception(f"Validation failed: {error_msg}")
                
                # 2. Check for duplicate primary key (basic check for now)
                schema = self.catalog.get_table_schema(table_name)
                if schema["primary_key"]:
                    pk_index = schema["column_order"].index(schema["primary_key"])
                    pk_value = values[pk_index]
                    
                    # Read existing rows to check for duplicates
                    existing_rows = self.storage.read_table(table_name)
                    for row in existing_rows:
                        if row[pk_index] == pk_value:
                            raise Exception(f"Duplicate primary key value: {pk_value}")
                
                # 3. Check unique constraints (basic check for now)
                for unique_col in schema.get("unique_columns", []):
                    col_index = schema["column_order"].index(unique_col)
                    col_value = values[col_index]
                    
                    existing_rows = self.storage.read_table(table_name)
                    for row in existing_rows:
                        if row[col_index] == col_value:
                            raise Exception(f"Duplicate value for UNIQUE column '{unique_col}': {col_value}")
                
                # 4. Insert the row
                rows = self.storage.read_table(table_name)
                rows.append(values)
                self.storage.write_table(table_name, rows)
                
                print(f"Inserted 1 row into {table_name}")
                
            except Exception as e:
                print(f"Error: {e}")
            return
        
        
        print(f"Command received: {command}")
        print("Supported: CREATE TABLE, INSERT INTO, SHOW TABLES, EXIT")

        