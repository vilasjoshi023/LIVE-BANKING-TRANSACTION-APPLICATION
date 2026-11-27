# Section 01 – NoSQL Fundamentals & Apache Cassandra Overview

**Master Program source section:** 1  
**Tracking status:** Not started as a structured module; concepts to be assessed and documented.

## Source syllabus topics

- What is NoSQL?
- Types of NoSQL Databases
- CAP vs PACELC
- BASE vs ACID
- Apache Cassandra Overview
- Cassandra vs RDBMS
- Modern use cases
- Real-world adopters

## Learning objective

Build a conceptual foundation for distributed NoSQL databases and explain where Cassandra fits.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Compare key-value, document, wide-column and graph database models using small examples.
2. Explain CAP and PACELC with a three-node network-partition thought experiment; distinguish these models from a specific Cassandra consistency-level choice.
3. Compare relational normalization and joins with Cassandra query-driven denormalization.
4. Map the Live Banking synthetic transaction workload to Cassandra's distributed architecture.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] NoSQL database-type comparison table.
- [ ] CAP/PACELC and BASE/ACID explanation with a VJCLAB example.
- [ ] Cassandra-vs-RDBMS interview answer.

## Interview checkpoint

- Why is Cassandra classified as a wide-column database?
- What is the difference between CAP and PACELC?
- Why is query-driven denormalization common in Cassandra?

## Safety and version controls

- Current learning baseline: CentOS Stream 9 and Apache Cassandra 4.1.12 on VJCLAB.
- Use synthetic data and bounded queries. Never expose credentials, password hashes, .env values, SSH keys or customer information.
- Do not perform destructive operations, node lifecycle changes, service restarts, repair, cleanup, major compactions, security changes or upgrades without a separate pre-check and maintenance plan.
- For Cassandra 5.x or modernization subjects, use a separate compatible test environment. Do not apply 5.x-only features to the current 4.1.12 cluster.
- Update this page only when execution evidence exists; a planned exercise is not a completed lab.

## Session log

| Date | Activity | Result/evidence | Status |
|---|---|---|---|
|  |  |  | Not started |
