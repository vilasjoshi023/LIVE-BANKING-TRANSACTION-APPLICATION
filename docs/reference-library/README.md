# Cassandra Reference Library

This folder contains searchable repository versions and page guides prepared from four user-provided PDF references.

## Source documents

| Source PDF | Pages | Repository reference | Coverage |
|---|---:|---|---|
| `cassandra performance tuning with solutions.pdf` | 115 | [Searchable page text](cassandra-performance-tuning-with-solutions-source-text.md) | Performance troubleshooting scenarios, read/write latency, compaction, tombstones, JVM, partition skew, capacity and interview answers |
| `cassandra performance tuning with solutions's.pdf` | 9 | [Page-by-page infographic guide](cassandra-production-scenarios-infographics-page-guide.md) | Nine visual production scenarios: general DBA experience, capacity planning, disk 95%, pending compactions, hot partition, JVM GC, tombstones, high write latency and high read latency |
| `Cassandra_Database_Administrator_Complete_Guide.pdf` | 62 | [Searchable page text](cassandra-database-administrator-complete-guide-source-text.md) | Cassandra 4.1.x DBA concepts, architecture, operations, backup/recovery, performance, security, monitoring and incidents |
| `Cassandra_DBA_Beginner_to_Advanced_Practical_Workbook.pdf` | 28 | [Searchable page text](cassandra-dba-beginner-to-advanced-practical-workbook-source-text.md) | Guided CentOS Stream 9 / Cassandra 4.1.12 lab roadmap, CQL, modeling, consistency, nodetool, repair, backup, performance, security and interview practice |

## Page-range navigation

The searchable transcriptions preserve source page markers. Use the headings `Source PDF page N` to navigate to the original page location.

The 9-page infographic PDF did not contain a machine-readable text layer. Its guide is a visual page summary, not a verbatim OCR transcription.

## Important file-format note

The repository currently contains the searchable Markdown transcriptions and the infographic page guide; it does **not** contain the original PDF binary attachments. The source PDFs remain in the conversation uploads. Exact visual fidelity, embedded graphics and original pagination are preserved only in those source PDFs. To keep the repository searchable and avoid presenting a text transcription as an identical PDF, this distinction is explicit.

## Source and version discipline

- The DBA guide and workbook identify Apache Cassandra 4.1.x as their main lab baseline; the workbook specifically lists CentOS Stream 9 and Cassandra 4.1.12.
- Validate commands and settings against the exact deployed Cassandra release and local package layout.
- Examples and thresholds in the performance documents are source examples, not measurements or production SLAs for VJCLAB.
- The security and operational work for VJCLAB is separately recorded in [the Cassandra security audit](../daily-activity/2026-11-25-cassandra-security-audit.md).


## Original PDF binaries

The original PDF files are **not yet present in the GitHub repository**. Their upload location, filenames, byte sizes and SHA-256 checksums are documented in [source-pdfs/README.md](source-pdfs/README.md). A prepared ZIP bundle containing the four original PDFs is intended to be extracted into this `docs/reference-library/` directory so that the files land in `source-pdfs/`. After extraction, commit and push that folder from a local clone.
