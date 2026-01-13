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
                
                # 2. Check for duplicate primary key using index
                schema = self.catalog.get_table_schema(table_name)
                if schema["primary_key"]:
                    pk_index = schema["column_order"].index(schema["primary_key"])
                    pk_value = values[pk_index]
                    
                    # Use index for faster duplicate check
                    index = self.catalog.get_index(table_name, schema["primary_key"])
                    if index and index.has_key(pk_value):
                        raise Exception(f"Duplicate primary key value: {pk_value}")
                    else:
                        # Fall back to full scan
                        existing_rows = self.storage.read_table(table_name)
                        for row in existing_rows:
                            if row[pk_index] == pk_value:
                                raise Exception(f"Duplicate primary key value: {pk_value}")
                
                # 3. Check unique constraints using indexes
                for unique_col in schema.get("unique_columns", []):
                    col_index = schema["column_order"].index(unique_col)
                    col_value = values[col_index]
                    
                    # Use index for faster duplicate check
                    index = self.catalog.get_index(table_name, unique_col)
                    if index and index.has_key(col_value):
                        raise Exception(f"Duplicate value for UNIQUE column '{unique_col}': {col_value}")
                    else:
                        # Fall back to full scan
                        existing_rows = self.storage.read_table(table_name)
                        for row in existing_rows:
                            if row[col_index] == col_value:
                                raise Exception(f"Duplicate value for UNIQUE column '{unique_col}': {col_value}")
                
                # 4. Insert the row
                rows = self.storage.read_table(table_name)
                row_position = len(rows)  # Position of new row
                rows.append(values)
                self.storage.write_table(table_name, rows)
                
                # 5. Update indexes
                # Update primary key index
                if schema["primary_key"]:
                    pk_index_col = schema["column_order"].index(schema["primary_key"])
                    pk_value = values[pk_index_col]
                    index = self.catalog.get_index(table_name, schema["primary_key"])
                    if index:
                        index.add(pk_value, row_position)
                
                # Update unique indexes
                for unique_col in schema.get("unique_columns", []):
                    col_index = schema["column_order"].index(unique_col)
                    col_value = values[col_index]
                    index = self.catalog.get_index(table_name, unique_col)
                    if index:
                        index.add(col_value, row_position)
                
                print(f"Inserted 1 row into {table_name}")
                
            except Exception as e:
                print(f"Error: {e}")
            return


        # SELECT command
        if cmd.upper().startswith("SELECT"):
            try:
                # Parse the SELECT command
                table_name, columns, where_clause = self.parser.parse_select(cmd)
                
                # Read the table data
                rows = self.storage.read_table(table_name)
                
                # Get schema for column mapping
                schema = self.catalog.get_table_schema(table_name)
                if not schema:
                    raise Exception(f"Table '{table_name}' not found")
                
                # Apply WHERE clause if present
                if where_clause:
                    column_name, operator, value = where_clause
                    
                    # Try to use index for fast lookup
                    index = self.catalog.get_index(table_name, column_name)
                    if index and operator == '=':
                        row_positions = index.get(value)
                        if row_positions:
                            # Read specific rows using positions
                            all_rows = self.storage.read_table(table_name)
                            rows = [all_rows[pos] for pos in row_positions if pos < len(all_rows)]
                        else:
                            rows = []  # No matches
                    else:
                        # Fall back to full table scan
                        col_index = schema["column_order"].index(column_name)
                        filtered_rows = []
                        for row in all_rows:
                            if row[col_index] == value:
                                filtered_rows.append(row)
                        rows = filtered_rows
                    
                # Select specific columns if requested
                if columns and columns != ['*']:
                    # Validate requested columns
                    for col in columns:
                        if col not in schema["column_order"]:
                            raise Exception(f"Column '{col}' not found in table '{table_name}'")
                    
                    # Map column names to indices
                    col_indices = [schema["column_order"].index(col) for col in columns]
                    
                    # Extract only requested columns
                    projected_rows = []
                    for row in rows:
                        projected_row = [row[idx] for idx in col_indices]
                        projected_rows.append(projected_row)
                    rows = projected_rows
                
                # Display results
                if not rows:
                    print("(0 rows)")
                else:
                    # Simple tabular display
                    for row in rows:
                        # Format the row for display
                        formatted_row = []
                        for value in row:
                            if isinstance(value, str):
                                formatted_row.append(f'"{value}"')
                            else:
                                formatted_row.append(str(value))
                        print(f"[{', '.join(formatted_row)}]")
                    print(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")
                    
            except Exception as e:
                print(f"Error: {e}")
            return

        if cmd.upper().startswith("UPDATE"):
            try:
                # Parse the UPDATE command
                table_name, updates, where_clause = self.parser.parse_update(cmd)
                
                # Read the table data
                rows = self.storage.read_table(table_name)
                
                # Get schema for validation
                schema = self.catalog.get_table_schema(table_name)
                if not schema:
                    raise Exception(f"Table '{table_name}' not found")
                
                # Validate updates against schema
                for column, new_value in updates.items():
                    if column not in schema["column_order"]:
                        raise Exception(f"Column '{column}' not found in table '{table_name}'")
                    
                    # Type checking
                    col_type = schema["columns"][column]
                    if col_type == "INT" and not isinstance(new_value, int):
                        raise Exception(f"Column '{column}' expects INT, got {type(new_value).__name__}")
                    elif col_type == "TEXT" and not isinstance(new_value, str):
                        raise Exception(f"Column '{column}' expects TEXT, got {type(new_value).__name__}")
                
                # Find rows to update
                rows_to_update = []
                if where_clause:
                    column_name, operator, value = where_clause
                    if column_name not in schema["column_order"]:
                        raise Exception(f"Column '{column_name}' not found in table '{table_name}'")
                    
                    col_index = schema["column_order"].index(column_name)
                    
                    for i, row in enumerate(rows):
                        if row[col_index] == value:
                            rows_to_update.append(i)
                else:
                    # Update all rows if no WHERE clause
                    rows_to_update = list(range(len(rows)))
                
                if not rows_to_update:
                    print(f"No rows matched the WHERE condition")
                    return
                
                # Apply updates and check constraints
                updated_count = 0
                for row_index in rows_to_update:
                    old_row = rows[row_index].copy()
                    new_row = old_row.copy()
                    
                    # Apply updates
                    for column, new_value in updates.items():
                        col_index = schema["column_order"].index(column)
                        new_row[col_index] = new_value
                    
                    # Check primary key uniqueness (if PK is being updated)
                    if schema["primary_key"] and schema["primary_key"] in updates:
                        pk_col = schema["primary_key"]
                        pk_index = schema["column_order"].index(pk_col)
                        new_pk_value = new_row[pk_index]
                        
                        # Check if new PK value already exists (excluding current row)
                        pk_index_obj = self.catalog.get_index(table_name, pk_col)
                        if pk_index_obj:
                            existing_positions = pk_index_obj.get(new_pk_value)
                            # Filter out current row's position
                            existing_positions = [pos for pos in existing_positions if pos != row_index]
                            if existing_positions:
                                raise Exception(f"Duplicate primary key value: {new_pk_value}")
                    
                    # Check unique constraints (if unique columns are being updated)
                    for unique_col in schema.get("unique_columns", []):
                        if unique_col in updates:
                            col_index = schema["column_order"].index(unique_col)
                            new_value = new_row[col_index]
                            
                            # Check if new value already exists (excluding current row)
                            unique_index = self.catalog.get_index(table_name, unique_col)
                            if unique_index:
                                existing_positions = unique_index.get(new_value)
                                # Filter out current row's position
                                existing_positions = [pos for pos in existing_positions if pos != row_index]
                                if existing_positions:
                                    raise Exception(f"Duplicate value for UNIQUE column '{unique_col}': {new_value}")
                    
                    # Update the row
                    rows[row_index] = new_row
                    updated_count += 1
                    
                    # Update indexes
                    # Update primary key index if PK changed
                    if schema["primary_key"] and schema["primary_key"] in updates:
                        pk_col = schema["primary_key"]
                        pk_index_pos = schema["column_order"].index(pk_col)
                        old_pk_value = old_row[pk_index_pos]
                        new_pk_value = new_row[pk_index_pos]
                        if old_pk_value != new_pk_value:
                            pk_index = self.catalog.get_index(table_name, pk_col)
                            if pk_index:
                                pk_index.update(old_pk_value, new_pk_value, row_index)
                    
                    # Update unique indexes if unique columns changed
                    for unique_col in schema.get("unique_columns", []):
                        if unique_col in updates:
                            col_index = schema["column_order"].index(unique_col)
                            old_value = old_row[col_index]
                            new_value = new_row[col_index]
                            if old_value != new_value:
                                unique_index = self.catalog.get_index(table_name, unique_col)
                                if unique_index:
                                    unique_index.update(old_value, new_value, row_index)
                
                # Write updated table back
                self.storage.write_table(table_name, rows)
                print(f"Updated {updated_count} row(s) in {table_name}")
                
            except Exception as e:
                print(f"Error: {e}")
            return
        
        if cmd.upper().startswith("DELETE FROM"):
            try:
                # Parse the DELETE command
                table_name, where_clause = self.parser.parse_delete(cmd)
                
                # Read the table data
                rows = self.storage.read_table(table_name)
                
                # Get schema
                schema = self.catalog.get_table_schema(table_name)
                if not schema:
                    raise Exception(f"Table '{table_name}' not found")
                
                # Find rows to delete
                rows_to_delete = []
                if where_clause:
                    column_name, operator, value = where_clause
                    if column_name not in schema["column_order"]:
                        raise Exception(f"Column '{column_name}' not found in table '{table_name}'")
                    
                    col_index = schema["column_order"].index(column_name)
                    
                    for i, row in enumerate(rows):
                        if row[col_index] == value:
                            rows_to_delete.append(i)
                else:
                    # Delete all rows if no WHERE clause
                    rows_to_delete = list(range(len(rows)))
                
                if not rows_to_delete:
                    print(f"No rows matched the WHERE condition")
                    return
                
                # Delete rows (from end to beginning to preserve indices)
                deleted_count = 0
                for row_index in sorted(rows_to_delete, reverse=True):
                    # Get the row before deleting
                    row = rows[row_index]
                    
                    # Remove from indexes
                    # Remove primary key from index
                    if schema["primary_key"]:
                        pk_col = schema["primary_key"]
                        pk_index = schema["column_order"].index(pk_col)
                        pk_value = row[pk_index]
                        pk_index_obj = self.catalog.get_index(table_name, pk_col)
                        if pk_index_obj:
                            pk_index_obj.remove(pk_value, row_index)
                    
                    # Remove unique columns from indexes
                    for unique_col in schema.get("unique_columns", []):
                        col_index = schema["column_order"].index(unique_col)
                        col_value = row[col_index]
                        unique_index = self.catalog.get_index(table_name, unique_col)
                        if unique_index:
                            unique_index.remove(col_value, row_index)
                    
                    # Delete the row
                    del rows[row_index]
                    deleted_count += 1
                    
                    # Update indexes for rows after the deleted one (shift positions)
                    # This is important: when we delete a row, all rows after it shift up
                    # So we need to update their positions in all indexes
                    for update_index in range(row_index, len(rows)):
                        # Update primary key index
                        if schema["primary_key"]:
                            pk_col = schema["primary_key"]
                            pk_index = schema["column_order"].index(pk_col)
                            pk_value = rows[update_index][pk_index]
                            pk_index_obj = self.catalog.get_index(table_name, pk_col)
                            if pk_index_obj:
                                # Remove old position, add new position
                                pk_index_obj.remove(pk_value, update_index + 1)  # Old position
                                pk_index_obj.add(pk_value, update_index)  # New position
                        
                        # Update unique indexes
                        for unique_col in schema.get("unique_columns", []):
                            col_index = schema["column_order"].index(unique_col)
                            col_value = rows[update_index][col_index]
                            unique_index = self.catalog.get_index(table_name, unique_col)
                            if unique_index:
                                unique_index.remove(col_value, update_index + 1)  # Old position
                                unique_index.add(col_value, update_index)  # New position
                
                # Write updated table back
                self.storage.write_table(table_name, rows)
                print(f"Deleted {deleted_count} row(s) from {table_name}")
                
            except Exception as e:
                print(f"Error: {e}")
            return

        print(f"Command received: {command}")
        print("Supported: CREATE TABLE, INSERT INTO, SHOW TABLES,SELECT,UPDATE, DELETE, EXIT")

        