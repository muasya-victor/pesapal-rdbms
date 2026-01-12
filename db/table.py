class Table:
    def __init__(self, schema, storage):
        self.schema = schema
        self.storage = storage
    
    def validate_insert(self, values):
        # 1. Check column count matches
        # 2. Check data types
        # 3. Check primary key uniqueness
        # 4. Check unique constraints
        pass
    
    def insert(self, values):
        if self.validate_insert(values):
            rows = self.storage.read_table(self.schema["name"])
            rows.append(values)
            self.storage.write_table(self.schema["name"], rows)