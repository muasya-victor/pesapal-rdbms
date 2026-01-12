from .tokenizer import tokenize

class Parser:
    def parse_create_table(self, sql):
        """
        Parse: CREATE TABLE table_name (col1 TYPE [CONSTRAINTS], ...)
        Returns: (table_name, columns)
        columns = [(col_name, col_type, [constraints]), ...]
        """
        tokens = tokenize(sql)
        
        # Basic validation
        if len(tokens) < 6:
            raise Exception("Invalid CREATE TABLE syntax")
        if tokens[0].upper() != "CREATE" or tokens[1].upper() != "TABLE":
            raise Exception("Not a CREATE TABLE statement")
        
        table_name = tokens[2]
        
        # Find parentheses
        try:
            open_paren = tokens.index('(')
            close_paren = tokens.index(')')
        except ValueError:
            raise Exception("Missing parentheses in CREATE TABLE")
        
        # Parse columns between parentheses
        column_tokens = tokens[open_paren + 1:close_paren]
        columns = self._parse_column_defs(column_tokens)
        
        return table_name, columns
    
    def _parse_column_defs(self, tokens):
        """
        Parse column definitions like:
        ['id', 'INT', 'PRIMARY', 'KEY', ',', 'email', 'TEXT', 'UNIQUE']
        Returns: [('id', 'INT', ['PRIMARY KEY']), ('email', 'TEXT', ['UNIQUE'])]
        """
        columns = []
        current_col = []
        
        for token in tokens:
            if token == ',':
                if current_col:
                    columns.append(self._parse_single_column(current_col))
                    current_col = []
            else:
                current_col.append(token)
        
        # Don't forget the last column
        if current_col:
            columns.append(self._parse_single_column(current_col))
        
        return columns
    
    def _parse_single_column(self, tokens):
        """
        Parse a single column definition like: ['id', 'INT', 'PRIMARY', 'KEY']
        Returns: ('id', 'INT', ['PRIMARY KEY'])
        """
        if len(tokens) < 2:
            raise Exception(f"Invalid column definition: {tokens}")
        
        col_name = tokens[0]
        col_type = tokens[1].upper()
        
        # Parse constraints (everything after type)
        constraint_tokens = tokens[2:]
        constraints = []
        
        i = 0
        while i < len(constraint_tokens):
            token = constraint_tokens[i].upper()
            
            if token == "PRIMARY":
                if i + 1 < len(constraint_tokens) and constraint_tokens[i + 1].upper() == "KEY":
                    constraints.append("PRIMARY KEY")
                    i += 2
                else:
                    raise Exception(f"Invalid PRIMARY constraint: {constraint_tokens}")
            elif token == "UNIQUE":
                constraints.append("UNIQUE")
                i += 1
            else:
                # Ignore unknown tokens (for now)
                i += 1
        
        return (col_name, col_type, constraints)