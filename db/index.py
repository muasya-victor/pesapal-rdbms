import json
from pathlib import Path

class HashIndex:
    """Simple hash-based index"""
    
    def __init__(self, index_name, storage):
        self.index_name = index_name
        self.storage = storage
        self.data = self._load_index()
    
    def _load_index(self):
        """Load index from disk"""
        index_path = self.storage.data_dir / f"{self.index_name}.idx"
        if not index_path.exists():
            return {}
        try:
            with open(index_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_index(self):
        """Save index to disk"""
        index_path = self.storage.data_dir / f"{self.index_name}.idx"
        with open(index_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add(self, key, row_position):
        """Add key -> row_position mapping"""
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(row_position)
        self._save_index()
    
    def remove(self, key, row_position):
        """Remove key -> row_position mapping"""
        if key in self.data:
            if row_position in self.data[key]:
                self.data[key].remove(row_position)
                if not self.data[key]:  # Empty list
                    del self.data[key]
            self._save_index()
    
    def update(self, old_key, new_key, row_position):
        """Update key mapping (for UPDATE operations)"""
        self.remove(old_key, row_position)
        self.add(new_key, row_position)
    
    def get(self, key):
        """Get row positions for a key"""
        return self.data.get(key, [])
    
    def has_key(self, key):
        """Check if key exists"""
        return key in self.data
    
    def clear(self):
        """Clear the index"""
        self.data = {}
        self._save_index()