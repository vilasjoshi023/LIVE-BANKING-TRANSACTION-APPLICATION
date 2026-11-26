# Original Cassandra PDF files

The original PDF attachments are packaged for upload into this directory. The repository currently contains searchable Markdown transcriptions and an infographic page guide in the parent folder; the original binary PDFs must be added from a local clone because the connected GitHub interface available to this workflow does not accept binary file attachments.

## Files to add

| PDF | Size (bytes) | SHA-256 |
|---|---:|---|
| `cassandra performance tuning with solutions.pdf` | 6914183 | `c2fab1d44f3a3b3deac2eb32cd92489fe12f881c93f8bbf8fe3446330f1e302b` |
| `cassandra performance tuning with solutions's.pdf` | 2546004 | `734109fbd8f3478ca8873521281f43637137da3d837085a5f1ae0348018b9e47` |
| `Cassandra_Database_Administrator_Complete_Guide.pdf` | 177677 | `bc1e02a5f211e07069d2fff1f777cf74b905d271ce660eadfb5c3f56ce444066` |
| `Cassandra_DBA_Beginner_to_Advanced_Practical_Workbook.pdf` | 94688 | `87d5b89826533faa8ef004a22eefd3e9f040bebb58173f2e990d979afc67c558` |

## Upload procedure

1. Download the ZIP bundle from the conversation.
2. Extract its `source-pdfs/` folder into this directory (the repository path is `docs/reference-library/source-pdfs/`).
3. From the repository root, run:

```bash
git status --short
git add docs/reference-library/source-pdfs/
git commit -m "docs: add original Cassandra PDF references"
git push origin main
```

4. Verify the four PDF files appear in this directory on GitHub.

The files are the original uploaded PDFs. Do not add passwords, .env files, private keys, database snapshots, SSTables or live application data.
