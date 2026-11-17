# Lab Safety, Evidence and Change Control

## Guardrails for the current lab
- Three CentOS Stream 9 VMs with roughly 3–3.5 GiB RAM each; do not overlap heavy repair, restore, compaction, upgrade or load tests.
- Use synthetic banking data only.
- Keep firewalld enabled; use only required, source-restricted rules.
- Keep Cassandra JMX 7199 local-only.
- Do not weaken SSH private-key permissions or distribute private keys unnecessarily.
- Never commit .env files, passwords, tokens, private keys, real customer data, raw Commit Logs, SSTables, snapshots or backup payloads.
- Never manually delete, move, truncate or rename Commit Log segments, hints or live SSTables.
- No repair, cleanup, scrub, compaction, decommission, removenode, snapshot deletion, restore-overwrite or upgrade on the working cluster without a reviewed scope and explicit approval.
- Do not enable live Commit Log archiving until callback semantics, no-clobber behavior, failure/retry handling, restore and PITR are validated in isolation.
- Leave the deferred VJC9LAB3 Linux account cleanup untouched unless specifically requested.

## Change record for each lab
1. Actual date/time and timezone.
2. Host/node, service, version and environment.
3. Objective and impact.
4. Pre-checks: node health, schema, disk, memory, ports, backup state and relevant metrics.
5. Exact command or configuration diff.
6. Expected output and abort conditions.
7. Execution output/logs with secrets redacted.
8. Post-checks and independent validation.
9. Rollback plan and whether rollback was tested.
10. Remaining risks and next action.

## Evidence scale
- **E0 – Topic listed:** no practical work.
- **E1 – Explained:** concept understood; no command run.
- **E2 – Executed:** command/code run and output recorded.
- **E3 – Validated:** expected result independently checked.
- **E4 – Repeatable:** procedure repeated successfully.
- **E5 – Operational runbook:** pre-check, change, rollback, monitoring and recovery validated in a suitable environment.

A written lesson is not automatically a completed practical lab.

## Stop conditions
Stop and investigate when a node is unexpectedly DN/joining/leaving; disk or memory headroom is unsafe; repair/compaction/streaming backlog grows; command scope differs from intended scope; output differs from expected; secret/customer data is about to be published; restore/upgrade might overwrite live data; or rollback is unclear.

## GitHub publication standard
Publish sanitised source, config templates, architecture diagrams, command examples, synthetic sample data and evidence summaries. Review each diff. Never publish secrets or database payloads.
