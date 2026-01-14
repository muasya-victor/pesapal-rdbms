# 🧪 Mini-RDBMS Test Instructions

## Quick Start (30 Seconds)

Run this single command to verify everything works:

```bash
python verify.py
```

**Expected:** Shows ✅ for all features and ends with "VERIFICATION COMPLETE"

## Interactive Demo (2 Minutes)

Start the interactive shell and try these commands:

```bash
python main.py
```

```sql
-- Create table with constraints
CREATE TABLE students (id INT PRIMARY KEY, name TEXT, grade INT)

-- Insert data
INSERT INTO students VALUES (1, "Alice", 85)
INSERT INTO students VALUES (2, "Bob", 92)

-- Query data
SELECT * FROM students
SELECT name FROM students WHERE grade > 90

-- Update data
UPDATE students SET grade = 95 WHERE name = "Alice"
SELECT * FROM students

-- Delete data
DELETE FROM students WHERE id = 2
SELECT * FROM students

-- Create related table and JOIN
CREATE TABLE courses (id INT PRIMARY KEY, name TEXT)
INSERT INTO courses VALUES (101, "Math")
INSERT INTO courses VALUES (102, "Science")

-- JOIN demonstration
SELECT students.name, courses.name  FROM students JOIN courses ON students.id = courses.id

-- Exit
EXIT
```

## Complete Test Suite

For detailed testing:

```bash
python test_all.py
```

## Features Demonstrated

| Feature | Example | Status |
|---------|---------|--------|
| **CREATE TABLE** | `CREATE TABLE t (id INT PRIMARY KEY)` | ✅ |
| **INSERT** | `INSERT INTO t VALUES (1, "test")` | ✅ |
| **SELECT** | `SELECT * FROM t WHERE id = 1` | ✅ |
| **UPDATE** | `UPDATE t SET name = "new" WHERE id = 1` | ✅ |
| **DELETE** | `DELETE FROM t WHERE id = 1` | ✅ |
| **JOIN** | `SELECT * FROM t1 JOIN t2 ON t1.id = t2.id` | ✅ |
| **Constraints** | PRIMARY KEY, UNIQUE enforcement | ✅ |
| **Indexes** | Automatic on constraints | ✅ |

## Troubleshooting

If tests fail:
1. Clear old data: `rm -rf data test_verify test_all_data`
2. Ensure Python 3.8+: `python --version`
3. Run from project root: `cd mini_rdbms`

## Project Structure

```
mini_rdbms/
├── verify.py     # Quick feature check (run this)
├── test_all.py   # Complete test suite
├── main.py      # Interactive shell
├── db/          # Storage engine
├── parser/      # SQL parser
├── executor/    # Query executor
└── repl/       # Command-line interface
```

## Success Criteria

The database works if:
1. `python verify.py` shows all ✅ checks
2. You can run the demo commands above
3. `python test_all.py` says "ALL TESTS PASSED"

---
