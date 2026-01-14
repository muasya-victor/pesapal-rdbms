┌────────────┐
│   REPL     │   ← Interactive shell
└─────┬──────┘
      ↓
┌────────────┐
│ SQL Parser │   ← SQL → AST conversion
└─────┬──────┘
      ↓
┌────────────┐
│  Executor  │   ← Query execution & validation
└─────┬──────┘
      ↓
┌────────────┐
│  Catalog   │   ← Schema & constraint management
└─────┬──────┘
      ↓
┌────────────┐
│  Storage   │   ← JSON file persistence
└────────────┘