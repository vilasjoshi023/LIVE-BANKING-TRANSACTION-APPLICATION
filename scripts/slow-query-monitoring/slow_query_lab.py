import csv
import math
import os
import time
from datetime import date, datetime

from src.cassandra_connection import get_cassandra_session

RUN_DATE = date(2026, 11, 18)
QUERIES_PER_TYPE = 50

QUERY_A = """
SELECT transaction_id, account_id, amount, created_at
FROM banking_stream.bank_transactions
WHERE transaction_date = ?
LIMIT 10
"""

QUERY_B = """
SELECT transaction_id, account_id, amount, created_at
FROM banking_stream.bank_transactions
WHERE transaction_date = ?
AND account_id = ?
LIMIT 10
ALLOW FILTERING
"""


def percentile(values, p):
    ordered = sorted(values)
    index = max(0, math.ceil(p * len(ordered)) - 1)
    return ordered[index]


def main():
    cluster = None

    try:
        print("Connecting to Cassandra...")
        cluster, session = get_cassandra_session()

        stmt_a = session.prepare(QUERY_A)
        stmt_b = session.prepare(QUERY_B)

        results = []

        print("Starting 100 sequential read queries...")

        for i in range(QUERIES_PER_TYPE):
            account_id = f"ACC{10000 + i}"

            queries = [
                ("A_PARTITION_LOOKUP", stmt_a, (RUN_DATE,)),
                ("B_ACCOUNT_FILTER", stmt_b, (RUN_DATE, account_id))
            ]

            for query_type, statement, parameters in queries:
                start = time.perf_counter()

                try:
                    rows = list(session.execute(statement, parameters))
                    latency = (time.perf_counter() - start) * 1000

                    result = {
                        "query_type": query_type,
                        "query_number": i + 1,
                        "account_id": account_id if query_type == "B_ACCOUNT_FILTER" else "",
                        "latency_ms": round(latency, 3),
                        "rows_returned": len(rows),
                        "status": "SUCCESS",
                        "error": ""
                    }

                except Exception as exc:
                    latency = (time.perf_counter() - start) * 1000

                    result = {
                        "query_type": query_type,
                        "query_number": i + 1,
                        "account_id": account_id,
                        "latency_ms": round(latency, 3),
                        "rows_returned": 0,
                        "status": "FAILED",
                        "error": str(exc).replace("\n", " ")[:300]
                    }

                results.append(result)

        log_dir = "/opt/banking-app/logs"
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(
            log_dir,
            f"slow_query_lab_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        with open(log_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "query_type",
                    "query_number",
                    "account_id",
                    "latency_ms",
                    "rows_returned",
                    "status",
                    "error"
                ]
            )
            writer.writeheader()
            writer.writerows(results)

        print("\n========== WORKLOAD SUMMARY ==========")
        print("Total queries:", len(results))
        print("Successful:", sum(r["status"] == "SUCCESS" for r in results))
        print("Failed:", sum(r["status"] == "FAILED" for r in results))

        for query_type in ["A_PARTITION_LOOKUP", "B_ACCOUNT_FILTER"]:
            group = [
                r for r in results
                if r["query_type"] == query_type
                and r["status"] == "SUCCESS"
            ]

            print(f"\n{query_type}")

            if not group:
                print("No successful queries")
                continue

            latencies = [r["latency_ms"] for r in group]

            print("Count:", len(group))
            print("Average:", round(sum(latencies) / len(latencies), 3), "ms")
            print("P50:", round(percentile(latencies, 0.50), 3), "ms")
            print("P95:", round(percentile(latencies, 0.95), 3), "ms")
            print("P99:", round(percentile(latencies, 0.99), 3), "ms")
            print("Maximum:", round(max(latencies), 3), "ms")

        print("\n========== TOP 10 SLOW QUERIES ==========")

        successful = [r for r in results if r["status"] == "SUCCESS"]

        for row in sorted(
            successful,
            key=lambda x: x["latency_ms"],
            reverse=True
        )[:10]:
            print(
                row["query_type"],
                "| Query:", row["query_number"],
                "| Account:", row["account_id"],
                "| Latency:", row["latency_ms"], "ms"
            )

        print("\nCSV report:", log_file)

        try:
            from src.slow_query_metrics_exporter import write_slow_query_metrics
            metrics_file = write_slow_query_metrics(results)
            print("Prometheus metrics file:", metrics_file)
        except Exception as exc:
            print("WARNING: Prometheus export failed:", exc)

    finally:
        if cluster is not None:
            cluster.shutdown()
            print("Cassandra connection closed.")


if __name__ == "__main__":
    main()
