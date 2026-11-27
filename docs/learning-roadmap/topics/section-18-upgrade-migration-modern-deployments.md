# Section 18 – Upgrade, Migration & Modern Deployments

**Master Program source section:** 18  
**Tracking status:** Not started; modernization and Cassandra 5.x activities deferred until core operations and recovery are validated.

## Source syllabus topics

- Rolling upgrades (4.x → 5.x)
- SSTable upgrades
- dsbulk / sstableloader
- Intro to Kubernetes (K8ssandra)
- Cloud Cassandra overview

## Learning objective

Plan version migration and modern deployment patterns without risking the active Cassandra 4.1.12 cluster.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Build Cassandra 4.1.12-to-5.x compatibility checklist for Java, config, drivers, SSTables, tools and upgrade order.
2. Review SSTable upgrade concepts and verify commands per release before use.
3. Compare dsbulk and sstableloader use cases for bulk load and migration.
4. Design isolated Cassandra 5.x validation before SAI or 4.x-to-5.x upgrade work.
5. Study K8ssandra and Kubernetes operator concepts; do not deploy on current memory-constrained VMs.
6. Compare self-managed Cassandra and cloud Cassandra operations.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Version compatibility matrix and upgrade/rollback plan.
- [ ] SSTable and bulk-load tool comparison.
- [ ] K8ssandra/cloud architecture notes; isolated test evidence if later executed.

## Interview checkpoint

- Why is a rolling upgrade not a package replacement?
- When would you use dsbulk versus sstableloader?
- Why must 5.x-only features be tested separately from 4.1.12?

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
