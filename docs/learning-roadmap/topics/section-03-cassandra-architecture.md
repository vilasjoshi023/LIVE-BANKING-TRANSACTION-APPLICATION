# Section 03 – Cassandra Architecture

**Master Program source section:** 3  
**Tracking status:** Three-node cluster and dc1 topology already exist; structured architecture walkthrough pending.

## Source syllabus topics

- Peer-to-peer architecture
- Ring & token distribution
- Nodes, DCs, clusters
- Gossip protocol (overview)
- Coordinator node
- Replication strategies
- Consistency levels (real scenarios)

## Learning objective

Explain how Cassandra distributes data and coordinates reads and writes across replicas.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Capture nodetool status, describecluster and gossipinfo from VJCLAB.
2. Map three nodes to dc1 and rack1; explain that same-rack VMs do not demonstrate rack failure-domain diversity.
3. Review vnode/token ownership and the coordinator role for a partition-key request.
4. Inspect NetworkTopologyStrategy replication for banking_stream and system_auth; explain RF=3 in dc1.
5. Work through ONE, QUORUM, LOCAL_QUORUM and ALL scenarios before any controlled failure test.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Annotated topology diagram with node IPs, DC and rack.
- [ ] Sanitized nodetool outputs and replication notes.
- [ ] Consistency-level scenario matrix.

## Interview checkpoint

- Is a seed node a master?
- What does gossip distribute?
- How does RF=3 work in a single three-node DC?
- Why does coordinator choice differ from replica ownership?

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
