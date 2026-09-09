```
GET /api/publications
        ↓
      PubMed
        ↓
   PMID found
        ↓
¿summary exist in SQLite?
   ↓ yes          ↓ no
SQLite       OpenAI one time
   ↓              ↓
   │          store in SQLite
   └──────┬───────┘
          ↓
        React
          ↓
     Lay Summary
   + View on PubMed
```

   Trials:

   ```
   Criteria
   ↓
Complicated?
   ↓
   NO ─────────→ show original
   ↓ YES
AI simplifier
   ↓
patient-friendly version
```
