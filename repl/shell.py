from db.storage import Storage
from db.catalog import Catalog
from parser.tokenizer import tokenize, parse_create_table
from executor.executor import Executor

class MiniDBShell:
    def __init__(self):
        self.running = True
        self.storage = Storage()
        self.catalog = Catalog(self.storage)
        self.executor = Executor(self.catalog, self.storage)
    
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
                tokens = tokenize(cmd)
                table_name, columns = parse_create_table(tokens)
                self.catalog.create_table(table_name, columns)
                print(f"Table '{table_name}' created successfully")
            except Exception as e:
                print(f"Error: {e}")
            return
        
        # SHOW TABLES command (useful for testing)
        if cmd.upper() == "SHOW TABLES":
            tables = self.catalog.list_tables()
            if tables:
                print("\n".join(tables))
            else:
                print("No tables exist")
            return
        
        if cmd.upper().startswith("INSERT INTO"):
            try:
                tokens = tokenize(cmd)
                
                table_name = tokens[2].upper()
                
                # Find VALUES keyword
                values_idx = tokens.index("VALUES")
                values_start = tokens.index('(', values_idx)
                values_end = tokens.index(')', values_start)
                
                # Extract values between parentheses
                value_tokens = tokens[values_start + 1:values_end]
                values = []
                for token in value_tokens:
                    if token == ',':
                        continue
                    # Remove quotes if present
                    if token.startswith('"') and token.endswith('"'):
                        values.append(token[1:-1])
                    else:
                        values.append(int(token))
                
                # Read existing rows, append new one, write back
                rows = self.storage.read_table(table_name)
                rows.append(values)
                self.storage.write_table(table_name, rows)
                
                print(f"Inserted 1 row into {table_name}")
                
            except Exception as e:
                print(f"Insert error: {e}")
            return
        
        # Unknown command
        print(f"Command received: {command}")
        print("Supported: CREATE TABLE, SHOW TABLES, SELECT 1, EXIT")

    def get_full_command(self):
        """Collect lines until semicolon"""
        lines = []
        while True:
            line = input("... " if lines else "mini-db> ")
            lines.append(line)
            if ';' in line:
                break
        return ' '.join(lines)