# Section 06 – Data Modeling – Advanced

**Master Program source section:** 6  
**Tracking status:** Planned; active banking schema remains unchanged.

## Source syllabus topics

- Time-series modeling
- Bucketing strategies
- Denormalization
- Handling large partitions

## Learning objective

Design scalable query tables for time-series and account-oriented transaction workloads.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Assess daily time-bucket partitioning in bank_transactions and project expected partition growth.
2. Design account_id plus time-bucket access patterns without unbounded scans.
3. Compare daily, hourly and fixed-size buckets using expected read range, write rate, partition size and retention.
4. Document denormalization trade-offs and how multiple query tables are kept consistent by the application.
5. Create candidate schema only in an isolated training keyspace after review; do not alter the active banking table.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Bucket-sizing worksheet.
- [ ] Two query-driven candidate schemas.
- [ ] Denormalization and write-amplification trade-off notes.

## Interview checkpoint

- When should a time-series partition be bucketed?
- How does denormalization affect write paths?
- What signals indicate an oversized or hot partition?

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
