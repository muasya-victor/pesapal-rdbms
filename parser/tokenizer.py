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