# Section 14 – Backup & Restore

**Master Program source section:** 14  
**Tracking status:** Snapshot/checksum/isolated SSTableLoader restore partly completed; off-host backup and full DR remain open.

## Source syllabus topics

- Snapshots & incremental backups
- Commit log backup
- Restore strategies
- Medusa overview

## Learning objective

Create verifiable backups and prove restore procedures against explicit RPO/RTO targets.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Review all-node snapshot banking_backup_20261116 and integrity-check history.
2. Document why a local snapshot is not an independent off-host backup.
3. Review SSTableLoader restore to banking_restore_lab.bank_transactions and 3,000-row partition validation.
4. Inspect incremental backup configuration and retention; do not delete existing snapshot data during practice.
5. Review CommitLog archive script v2 using dummy-file evidence only; live archive configuration remains disabled.
6. Study Medusa architecture and compatibility before installation.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Backup inventory, checksums and retention plan.
- [ ] Restore validation with row-count/sample comparison.
- [ ] RPO/RTO worksheet and Medusa evaluation.

## Interview checkpoint

- Why is a snapshot alone not a complete DR strategy?
- What does SSTableLoader do?
- How do RPO and RTO differ?

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
