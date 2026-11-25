import math
import os
import tempfile
import time

METRICS_DIR = "/var/lib/node_exporter/textfile_collector"
METRICS_FILE = os.path.join(
    METRICS_DIR, "banking_slow_query.prom"
)

SLOW_THRESHOLD_MS = 100.0


def percentile(values, p):
    ordered = sorted(values)
    index = max(0, math.ceil(p * len(ordered)) - 1)
    return ordered[index]


def write_slow_query_metrics(results):
    metric_help = {
        "banking_slow_query_last_run_requests": "Query attempts in latest run",
        "banking_slow_query_last_run_successes": "Successful queries in latest run",
        "banking_slow_query_last_run_errors": "Failed queries in latest run",
        "banking_slow_query_last_run_slow_requests": "Successful queries at or above 100ms",
        "banking_slow_query_last_run_rows_returned": "Rows returned in latest run",
        "banking_slow_query_last_run_latency_ms_avg": "Average query latency in ms",
        "banking_slow_query_last_run_latency_ms_p50": "P50 query latency in ms",
        "banking_slow_query_last_run_latency_ms_p95": "P95 query latency in ms",
        "banking_slow_query_last_run_latency_ms_p99": "P99 query latency in ms",
        "banking_slow_query_last_run_latency_ms_max": "Maximum query latency in ms",
        "banking_slow_query_last_run_timestamp_seconds": "Latest test run Unix timestamp",
    }

    lines = []
    for name, description in metric_help.items():
        lines.append(f"# HELP {name} {description}")
        lines.append(f"# TYPE {name} gauge")

    timestamp = time.time()

    for query_type in ("A_PARTITION_LOOKUP", "B_ACCOUNT_FILTER"):
        group = [r for r in results if r["query_type"] == query_type]
        successful = [r for r in group if r["status"] == "SUCCESS"]

        latencies = [
            float(r["latency_ms"])
            for r in successful
            if math.isfinite(float(r["latency_ms"]))
        ]

        values = {
            "banking_slow_query_last_run_requests": len(group),
            "banking_slow_query_last_run_successes": len(successful),
            "banking_slow_query_last_run_errors": len(group) - len(successful),
            "banking_slow_query_last_run_slow_requests":
                sum(v >= SLOW_THRESHOLD_MS for v in latencies),
            "banking_slow_query_last_run_rows_returned":
                sum(int(r["rows_returned"]) for r in successful),
            "banking_slow_query_last_run_timestamp_seconds": timestamp,
        }

        if latencies:
            values.update({
                "banking_slow_query_last_run_latency_ms_avg":
                    sum(latencies) / len(latencies),
                "banking_slow_query_last_run_latency_ms_p50":
                    percentile(latencies, 0.50),
                "banking_slow_query_last_run_latency_ms_p95":
                    percentile(latencies, 0.95),
                "banking_slow_query_last_run_latency_ms_p99":
                    percentile(latencies, 0.99),
                "banking_slow_query_last_run_latency_ms_max":
                    max(latencies),
            })

        for metric, value in values.items():
            lines.append(
                f'{metric}{{query_type="{query_type}"}} {value:.6f}'
            )

    os.makedirs(METRICS_DIR, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(
        prefix=".banking_slow_query_",
        suffix=".tmp",
        dir=METRICS_DIR
    )

    try:
        with os.fdopen(fd, "w") as handle:
            handle.write("\n".join(lines) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

        os.chmod(temp_path, 0o644)
        os.replace(temp_path, METRICS_FILE)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return METRICS_FILE
