# Section 09 – Indexing & Query Optimization

**Master Program source section:** 9  
**Tracking status:** Slow-query comparison already practiced; structured optimization review in progress.

## Source syllabus topics

- Primary key indexing
- Secondary index limits
- SAI (Cassandra 5.x)
- Query anti-patterns

## Learning objective

Choose query and indexing strategies that avoid broad scans, inefficient filtering and inappropriate indexes.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Review primary-key access patterns and current bank_transactions queries.
2. Explain limitations and workload trade-offs of secondary indexes; avoid adding indexes without a measured use case.
3. Review the slow-query comparison between partition lookup and bounded account filtering.
4. Record latency distributions and returned-row counts; distinguish observed correlation from proven root cause.
5. Study SAI as a Cassandra 5.x topic only; do not attempt SAI on the 4.1.12 lab.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Query anti-pattern catalogue.
- [ ] Slow-query comparison with test conditions.
- [ ] Index selection rationale; 5.x SAI lab deferred.

## Interview checkpoint

- Why is ALLOW FILTERING risky at scale?
- When would a second query table be preferable to an index?
- Which Cassandra version is required for SAI in this syllabus?

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
