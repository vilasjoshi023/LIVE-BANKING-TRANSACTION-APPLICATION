# Section 16 – Monitoring & Observability

**Master Program source section:** 16  
**Tracking status:** Monitoring stack and custom metrics present; scheduled workload paused for security maintenance; dashboard/alert deployment to verify.

## Source syllabus topics

- Metrics (latency, throughput, compaction)
- Logs (system.log, gc.log)
- Alerting strategies

## Learning objective

Correlate database, JVM, host and application metrics to detect and explain operational risks.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Inventory Prometheus, Node Exporter, Cassandra JMX Exporter and Grafana endpoints and scrape targets.
2. Review node health, read/write latency, dropped messages, pending compactions, disk, heap and GC signals.
3. Inspect system.log and GC log patterns and correlate timestamps with workload measurements.
4. Review custom slow-query textfile exporter and confirm metric freshness/error signals.
5. Validate prepared Grafana dashboard and alert templates separately; do not describe templates as active alerts.
6. Create alert runbooks with owner, severity, baseline, threshold and escalation path.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Monitoring architecture diagram and target status.
- [ ] Dashboard panel/query validation.
- [ ] Alert rule tests and runbook references.

## Interview checkpoint

- Why combine application and Cassandra metrics?
- What does a stale metric alert detect?
- Why should thresholds be based on a baseline?

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
