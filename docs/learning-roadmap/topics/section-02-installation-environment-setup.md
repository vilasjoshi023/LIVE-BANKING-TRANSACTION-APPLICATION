# Section 02 – Installation & Environment Setup

**Master Program source section:** 2  
**Tracking status:** Existing CentOS Stream 9 / Cassandra 4.1.12 lab is installed; review and validate rather than reinstall.

## Source syllabus topics

- Install Cassandra (Binary / Package)
- Single-node & multi-node setup
- cassandra.yaml basics
- OS tuning (ulimits, disk, memory)
- cqlsh basics (CREATE / INSERT / SELECT)
- nodetool (status, ring)

## Learning objective

Understand how Cassandra is installed, configured and operated on Linux without unnecessarily rebuilding the existing lab.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Inventory Java, Cassandra paths, systemd units, data directories and configuration files on all three VMs.
2. Review cassandra.yaml: cluster name, seeds, listen_address, rpc_address, native transport port and snitch.
3. Record CPU, RAM, swap, filesystems, open-file limits, time synchronization and network ports on each VM.
4. Review cqlsh connectivity and basic CREATE/INSERT/SELECT in a disposable training keyspace.
5. Compare installed settings with a Cassandra 4.1.12 reference; do not overwrite node-specific values.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Timestamped three-node environment inventory.
- [ ] Sanitized configuration summary and OS baseline.
- [ ] Successful bounded cqlsh and nodetool status checks.

## Interview checkpoint

- What is the purpose of seeds?
- What is the difference between listen_address and rpc_address?
- Which OS limits and resource metrics matter to Cassandra?

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
