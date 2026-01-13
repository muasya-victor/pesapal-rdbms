# repl/shell.py
from db.storage import Storage
from db.catalog import Catalog
from parser.tokenizer import tokenize
from executor.executor import Executor
from parser.parser import Parser
import builtins


class MiniDBShell:
    def __init__(self):
        self.running = True
        self.storage = Storage()
        self.catalog = Catalog(self.storage)
        self.executor = Executor(self.catalog, self.storage)
        self.parser = Parser()

    def execute(self, command: str) -> str:
        output = []

        def write(*args, **kwargs):
            output.append(" ".join(map(str, args)))

        original_print = builtins.print
        builtins.print = write

        try:
            self.handle_command(command)
        finally:
            builtins.print = original_print

        return "\n".join(output)

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
                result = self.executor.execute_create_table(table_name, columns)
                print(result)
            except Exception as e:
                print(f"Error: {e}")
            return
        
        # SHOW TABLES command
        if cmd.upper() == "SHOW TABLES":
            try:
                result = self.executor.execute_show_tables()
                print(result)
            except Exception as e:
                print(f"Error: {e}")
            return
        
        # INSERT command
        if cmd.upper().startswith("INSERT INTO"):
            try:
                # Parse the INSERT command
                table_name, values = self.parser.parse_insert(cmd)
                result = self.executor.execute_insert(table_name, values)
                print(result)
            except Exception as e:
                print(f"Error: {e}")
            return

        # SELECT command
        if cmd.upper().startswith("SELECT"):
            try:
                # Parse the SELECT command
                table_info, columns, where_clause = self.parser.parse_select(cmd)
                rows = self.executor.execute_select(table_info, columns, where_clause)
                result = self.executor.format_results(rows)
                print(result)
            except Exception as e:
                print(f"Error: {e}")
            return
        
        # UPDATE command
        if cmd.upper().startswith("UPDATE"):
            try:
                # Parse the UPDATE command
                table_name, updates, where_clause = self.parser.parse_update(cmd)
                result = self.executor.execute_update(table_name, updates, where_clause)
                print(result)
            except Exception as e:
                print(f"Error: {e}")
            return
        
        # DELETE command
        if cmd.upper().startswith("DELETE FROM"):
            try:
                # Parse the DELETE command
                table_name, where_clause = self.parser.parse_delete(cmd)
                result = self.executor.execute_delete(table_name, where_clause)
                print(result)
            except Exception as e:
                print(f"Error: {e}")
            return

        # Unknown command
        print(f"Command received: {command}")
        print("Supported: CREATE TABLE, INSERT INTO, SHOW TABLES, SELECT, UPDATE, DELETE, EXIT")