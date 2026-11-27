# Section 07 – Cassandra Query Language (CQL) – Basics

**Master Program source section:** 7  
**Tracking status:** CQL already used for the project; structured basic-to-advanced lab remains.

## Source syllabus topics

- CQL Overview (DDL, DML, DCL and differences from SQL)
- CRUD operations with best practices for partition keys and clustering keys
- TTL & collections

## Learning objective

Use CQL safely for schema inspection, data manipulation and keyspace/table operations.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Practice DESCRIBE KEYSPACE, DESCRIBE TABLE and system_schema metadata queries.
2. Create a disposable keyspace/table and practice INSERT, SELECT, UPDATE and DELETE with full primary-key predicates.
3. Compare CQL DDL, DML and DCL with relational SQL terminology.
4. Practice TTL on disposable records and inspect expiry/tombstone implications.
5. Use collection types only for bounded attributes; discuss collection growth risks.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] CQL command log with sanitized output.
- [ ] Disposable schema and CRUD validation.
- [ ] TTL behavior notes and collection design review.

## Interview checkpoint

- Why must a CQL query include the partition key?
- What is the impact of TTL?
- How does CQL differ from SQL?

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
