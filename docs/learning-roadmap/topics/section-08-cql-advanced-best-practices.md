# Section 08 – Cassandra Query Language (CQL) – Advanced & Best Practices

**Master Program source section:** 8  
**Tracking status:** Planned; use low-load, bounded tests due to VM resource constraints.

## Source syllabus topics

- Batches (good vs bad)
- Prepared statements
- LWT (when to avoid)
- Query tracing & Consistency levels in queries

## Learning objective

Choose advanced CQL features based on correctness, latency and workload characteristics.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Review Python driver execution and identify statements suitable for prepared statements.
2. Compare a logged batch for justified atomicity with an inappropriate large cross-partition batch.
3. Explain LWT/Paxos cost and identify a synthetic example where conditional writes are justified.
4. Use cqlsh TRACING for a bounded partition-key query and inspect trace stages.
5. Compare per-query consistency settings with the session default LOCAL_QUORUM.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Prepared-statement example and timing comparison.
- [ ] Batch decision worksheet.
- [ ] Trace output and consistency-level decision matrix.

## Interview checkpoint

- When is a batch appropriate?
- Why can LWT be more expensive than a normal write?
- What can tracing reveal that client latency alone cannot?

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
