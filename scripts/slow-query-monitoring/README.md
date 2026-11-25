# Cassandra Slow-Query Monitoring Scripts

This folder contains the source and deployment unit files for the synthetic 100-query monitoring exercise in the Live Banking Transaction Application.

## Files

- `slow_query_lab.py`: Executes 100 sequential read queries per run: 50 date-partition lookups and 50 bounded account-filter queries. Records per-query duration, rows, status and error text in a timestamped CSV file. Prints average, P50, P95, P99, maximum and the ten slowest successful requests.
- `slow_query_metrics_exporter.py`: Publishes latest-run aggregate metrics to the Node Exporter textfile collector.
- `banking-slow-query.service`: systemd oneshot service to run the Python workload.
- `banking-slow-query.timer`: systemd timer template with a two-minute boot delay and a five-minute interval after each service run.

## Runtime assumptions

The scripts are designed for the lab paths and environment currently used on VJC9LAB1:

- Application root: `/opt/banking-app`
- Python virtual environment: `/opt/banking-app/venv`
- Cassandra connection factory: `src.cassandra_connection.get_cassandra_session()`
- Keyspace/table: `banking_stream.bank_transactions`
- Test partition date: `2026-11-18`
- Node Exporter textfile directory: `/var/lib/node_exporter/textfile_collector`
- Metrics file: `banking_slow_query.prom`
- CSV output directory: `/opt/banking-app/logs`

The application repository must include the existing `src/cassandra_connection.py` module and its locally configured environment file. Do not commit credentials or the environment file.

## Query patterns

### Query A – partition-key lookup

Filters by the table partition key `transaction_date`.

### Query B – account filtering inside one date partition

Filters by `transaction_date` and `account_id`. Since `account_id` is not part of the table primary key, the query uses `ALLOW FILTERING` and a `LIMIT 10` within one known date partition. This is a deliberately bounded lab anti-pattern used for comparison, not a production recommendation. A production account-history access pattern should be designed around an appropriate account-based partition key or query table.

## Metrics exported

All metrics are gauges describing the **latest completed batch**, separated by the bounded `query_type` label:

- `banking_slow_query_last_run_requests`
- `banking_slow_query_last_run_successes`
- `banking_slow_query_last_run_errors`
- `banking_slow_query_last_run_slow_requests`
- `banking_slow_query_last_run_rows_returned`
- `banking_slow_query_last_run_latency_ms_avg`
- `banking_slow_query_last_run_latency_ms_p50`
- `banking_slow_query_last_run_latency_ms_p95`
- `banking_slow_query_last_run_latency_ms_p99`
- `banking_slow_query_last_run_latency_ms_max`
- `banking_slow_query_last_run_timestamp_seconds`

The initial slow-request threshold is 100 ms. This is a lab setting, not an SLA. Account IDs and transaction details are deliberately not used as Prometheus labels.

Because these are latest-run gauges, Prometheus stores samples over time as it scrapes. The metrics do not represent lifetime cumulative counts or true per-query histograms.

## Deployment outline

Copy the two Python modules into the existing application's `src/` directory, preserving the package structure:

```bash
install -m 0644 slow_query_lab.py /opt/banking-app/src/slow_query_lab.py
install -m 0644 slow_query_metrics_exporter.py /opt/banking-app/src/slow_query_metrics_exporter.py
cd /opt/banking-app
/opt/banking-app/venv/bin/python -m py_compile src/slow_query_lab.py src/slow_query_metrics_exporter.py
```

Install unit files on VJC9LAB1:

```bash
install -m 0644 banking-slow-query.service /etc/systemd/system/banking-slow-query.service
install -m 0644 banking-slow-query.timer /etc/systemd/system/banking-slow-query.timer
systemctl daemon-reload
systemd-analyze verify /etc/systemd/system/banking-slow-query.service /etc/systemd/system/banking-slow-query.timer
```

Validate manually before enabling recurring execution:

```bash
systemctl start banking-slow-query.service
journalctl -u banking-slow-query.service -n 50 --no-pager
```

The five-minute timer is intentionally **not enabled by this repository change**. Enable it on the lab host only after confirming readiness for recurring synthetic read traffic:

```bash
systemctl enable --now banking-slow-query.timer
systemctl list-timers banking-slow-query.timer --no-pager
```

## Operational cautions

- The workload performs reads only; it does not insert, update or delete transactions.
- It runs 100 sequential requests per batch and should remain bounded in this resource-constrained three-node lab.
- The service template runs as root, matching the manually tested service and allowing it to write the root-owned textfile metric. Revisit least-privilege permissions before adapting it for production.
- The timer is designed to schedule the next batch after the previous oneshot service completes. Check service duration and timer state before shortening the interval.
- Keep CSV reports free of sensitive values. The test records account IDs from synthetic lab data; do not use real customer identifiers.
- This is a learning and monitoring harness, not a production banking load generator, a production slow-query log replacement, or an SLA measurement system.
