# Section 11 – Multi-Node Cluster Setup and Operations

**Master Program source section:** 11  
**Tracking status:** Existing three-node cluster operating; lifecycle practice remains planned.

## Source syllabus topics

- Initializing a cluster (3 nodes) with proper seed nodes
- Single DC vs Multi-DC setup using NetworkTopologyStrategy
- Gossip and RPC configuration
- Testing consistency levels and data distribution
- Node lifecycle: Bootstrap, Decommission, Replace, Move, Removenode

## Learning objective

Operate a multi-node topology safely and understand node lifecycle transitions.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Document VJCLAB seed configuration, DC/rack topology and internode/native transport endpoints.
2. Compare SimpleStrategy with NetworkTopologyStrategy; explain system_auth update to NetworkTopologyStrategy dc1=3.
3. Review gossip and schema agreement through nodetool describecluster and gossipinfo.
4. Use a disposable keyspace to reason about RF and distribution; avoid topology experiments against banking_stream.
5. Build runbooks for bootstrap, decommission, replace, move and removenode; execute only in a separate disposable cluster or approved isolated exercise.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Three-node topology diagram and configuration comparison.
- [ ] Gossip/schema agreement evidence.
- [ ] Node lifecycle runbooks with prechecks and abort conditions.

## Interview checkpoint

- What happens during bootstrap?
- Why is decommission safer than deleting node data?
- How does NetworkTopologyStrategy place replicas?

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
