# 🧪 Mini-RDBMS Test Instructions

## Quick Verification (30 seconds)

Run this single command to verify all features:

```bash
python verify.py
```

**Expected output:** Shows ✅ for all features and ends with "VERIFICATION COMPLETE"

## Complete Test Suite (2 minutes)

For a more detailed test:

```bash
python test_all.py
```

**What it tests:**
1. ✅ CREATE TABLE with constraints (PRIMARY KEY, UNIQUE)
2. ✅ INSERT with type validation
3. ✅ SELECT with WHERE clause
4. ✅ UPDATE and DELETE operations
5. ✅ JOIN between tables
6. ✅ Automatic indexing
7. ✅ Complete workflow demo

## Interactive Demo

After successful tests, try the interactive shell:

```bash
python main.py
```

**Sample session:**
```
muasya-rdbms> CREATE TABLE students (id INT PRIMARY KEY, name TEXT, grade INT)
muasya-rdbms> INSERT INTO students VALUES (1, "Alice", 85)
muasya-rdbms> INSERT INTO students VALUES (2, "Bob", 92)
muasya-rdbms> SELECT * FROM students
muasya-rdbms> EXIT
```

## Project Structure

```
mini_rdbms/
├── verify.py          # ✅ Quick verification (run this first)
├── test_all.py        # ✅ Complete test suite
├── main.py           # ▶️ Interactive shell
├── db/               # Storage, catalog, indexes
├── parser/           # SQL parsing
├── executor/         # Query execution
├── repl/            # Interactive REPL
└── data/            # Persisted data (created automatically)
```

## Features Verified

| Feature | Status | Verified By |
|---------|--------|-------------|
| SQL-like syntax | ✅ | CREATE/INSERT/SELECT/UPDATE/DELETE/JOIN |
| Constraints | ✅ | PRIMARY KEY, UNIQUE, type validation |
| Indexing | ✅ | Automatic hash indexes |
| JOIN operations | ✅ | INNER JOIN with equality |
| Persistent storage | ✅ | JSON file storage |
| Interactive REPL | ✅ | Terminal interface |

## Troubleshooting

If tests fail:
1. **Clear old data:** `rm -rf data/`
2. **Check Python version:** Requires Python 3.8+
3. **Re-run:** `python verify.py`

## Success Criteria

The database is working correctly if:
1. `python verify.py` shows all ✅ checks
2. `python test_all.py` ends with "ALL TESTS PASSED"
3. `python main.py` allows you to run sample SQL commands

---

---
# NOTE
All test data is in /data
---
