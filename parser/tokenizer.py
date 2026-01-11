def tokenize(sql):
    """Super simple tokenizer - split by whitespace and special chars"""
    tokens = []
    current = ''
    
    for char in sql:
        if char in ' ;(),=':
            if current:
                tokens.append(current)
                current = ''
            if char != ' ':
                tokens.append(char)
        else:
            current += char
    
    if current:
        tokens.append(current)
    
    return tokens

def parse_create_table(tokens):
    """
    Parse: CREATE TABLE table_name (col1 TYPE, col2 TYPE)
    Returns: (table_name, columns)
    columns = [("col1", "TYPE"), ("col2", "TYPE")]
    """
    # Skip CREATE, TABLE
    if len(tokens) < 6:
        raise Exception("Invalid CREATE TABLE syntax")
    
    table_name = tokens[2]  # Third token
    
    # Find parentheses
    try:
        open_paren = tokens.index('(')
        close_paren = tokens.index(')')
    except ValueError:
        raise Exception("Missing parentheses in CREATE TABLE")
    
    # Parse columns between parentheses
    column_tokens = tokens[open_paren + 1:close_paren]
    columns = []
    
    i = 0
    while i < len(column_tokens):
        if column_tokens[i] == ',':
            i += 1
            continue
        
        col_name = column_tokens[i]
        if i + 1 >= len(column_tokens):
            raise Exception(f"Missing type for column {col_name}")
        
        col_type = column_tokens[i + 1].upper()
        if col_type not in ['INT', 'TEXT']:
            raise Exception(f"Unsupported type: {col_type}")
        
        columns.append((col_name, col_type))
        i += 2
    
    return table_name, columns