# Section 05 – Data Modeling – Fundamentals

**Master Program source section:** 5  
**Tracking status:** bank_transactions schema and slow-query pattern are known; modeling assessment pending.

## Source syllabus topics

- Query-driven design
- Partition vs Clustering key
- Primary key design
- Avoid hotspots & large partitions

## Learning objective

Design tables around required access patterns and understand partition distribution and clustering order.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Review banking_stream.bank_transactions: partition key transaction_date and clustering key transaction_id.
2. List supported query patterns and identify which require a full partition key.
3. Explain why account_id filtering is not a primary-key lookup and why bounded ALLOW FILTERING is a lab anti-pattern, not production guidance.
4. Estimate rows and bytes per daily partition from observed synthetic workload volume.
5. Design on paper a separate account-oriented query table for account transaction history.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Existing table schema and query-pattern inventory.
- [ ] Partition-size estimate with assumptions.
- [ ] Proposed account-oriented table design.

## Interview checkpoint

- What is a partition key?
- What is the role of clustering columns?
- Why should a Cassandra table be designed from query patterns?

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
