def tokenize(sql):
    """
    Tokenizer that handles:
    - Quoted strings: "hello world"
    - Multiple spaces
    - Special characters: ( ) , = ;
    """
    tokens = []
    current = ''
    in_quotes = False
    quote_char = None
    
    i = 0
    while i < len(sql):
        char = sql[i]
        
        # Handle quotes
        if char in ('"', "'") and (i == 0 or sql[i-1] != '\\'):
            if not in_quotes:
                # Start of quoted string
                in_quotes = True
                quote_char = char
                if current:  # Flush any previous token
                    tokens.append(current)
                    current = ''
                current += char
            elif char == quote_char:
                # End of quoted string
                current += char
                tokens.append(current)
                current = ''
                in_quotes = False
                quote_char = None
            else:
                # Nested or mismatched quote - treat as normal char
                current += char
        elif in_quotes:
            # Inside quoted string, add everything
            current += char
        elif char in ' ;(),=':
            # Special characters that break tokens
            if current:
                tokens.append(current)
                current = ''
            if char != ' ':
                tokens.append(char)
        else:
            # Regular character
            current += char
        
        i += 1
    
    # The last token
    if current:
        tokens.append(current)
    
    return tokens