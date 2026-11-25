# Project Script Library

This directory contains version-controlled scripts and supporting configuration templates for the Live Banking Transaction Application lab.

## Script collections

- [Cassandra slow-query monitoring](slow-query-monitoring/README.md) – 100-query synthetic read workload, per-run CSV latency report, Prometheus textfile exporter, and systemd service/timer templates.

## Usage and safety

- Read the folder-specific README before deployment.
- Verify the target host paths, service account, permissions, Python environment and monitoring collector configuration.
- Test scripts manually and validate outputs before enabling any timer or scheduled job.
- Do not commit passwords, API tokens, private SSH keys, `.env` files, real customer data, raw Commit Logs, SSTables, snapshots or backup directories.
- These scripts are lab tooling. Validate and harden them for the target environment before any production use.
