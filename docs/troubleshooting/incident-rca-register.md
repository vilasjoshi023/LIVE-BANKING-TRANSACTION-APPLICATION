# Project Issue Register – Errors, RCA and Corrective Actions

This register captures errors and operational problems documented during the VJCLAB lab. It distinguishes confirmed root causes from likely causes, general troubleshooting guidance and unresolved findings. It is a record of lab engineering work, not a claim that every listed symptom was encountered as a production incident.

## RCA method used

For each issue, follow this sequence:

1. Capture the exact symptom and the command/output that demonstrates it.
2. Establish scope: one process, one VM, one port, one node, or the complete cluster.
3. Check service state and listener binding before changing configuration.
4. Test the network path and inspect firewalld/SELinux policy where applicable.
5. Check application invocation, environment and permissions.
6. Identify the smallest root cause supported by evidence.
7. Apply a targeted correction; avoid broad changes such as disabling firewalld or SELinux.
8. Re-run the failing check and a higher-level end-to-end validation.
9. Record the result and any remaining limitations.

## Confirmed issues and resolution record

### RCA-001 – Node Exporter queried through localhost

**Symptom:** A local `curl` request to `http://localhost:9100/metrics` failed even though Node Exporter was running.

**Investigation:** Inspected the listener with `ss -lntp` and verified the service's configured bind address.

**Root cause:** Node Exporter was listening on the VM's specific address (for example, `192.168.62.134:9100`), not on loopback.

**Corrective action:** Query the actual node address, such as `curl http://192.168.62.134:9100/metrics`.

**Validation:** Metrics were returned from each of the three node IP addresses. This was a bind-address mismatch, not evidence that Node Exporter was down.

### RCA-002 – No route to host on TCP/9100

**Symptom:** Ping to the node succeeded, but a TCP connection to Node Exporter port 9100 failed with `No route to host`.

**Investigation:** Checked `firewall-cmd --state`, `--get-active-zones` and `--list-all`. The active zone was `public`, and TCP/9100 was not permitted.

**Root cause:** Host firewall policy blocked the exporter port even though basic ICMP connectivity worked.

**Corrective action:** Added source-restricted firewalld rich rules for the required lab IPs and reloaded firewalld. On the monitoring host the rule sources were the three lab VMs; on the two remote nodes the permitted source was the Prometheus host (LAB1). Firewalld was not disabled.

**Validation:** From LAB1, queried the three `http://<node-ip>:9100/metrics` endpoints and received metrics.

**Operational learning:** ICMP reachability does not prove that a TCP service port is reachable. Validate the relevant TCP port and active firewall zone.

### RCA-003 – Prometheus localhost health check failed

**Symptom:** `curl http://localhost:9090/-/healthy` failed.

**Investigation:** Checked the Prometheus listening socket with `ss -lntp`.

**Root cause:** Prometheus was bound to `192.168.62.134:9090`, not localhost.

**Corrective action:** Used the configured address: `curl http://192.168.62.134:9090/-/healthy`, followed by the `/-/ready` endpoint.

**Validation:** Health and readiness endpoints returned their expected success messages. The target inventory later showed seven targets UP.

### RCA-004 – Grafana could not query Prometheus because of SELinux

**Symptom:** Grafana datasource connectivity/Explore queries to Prometheus were denied even though Prometheus was listening and reachable from the host.

**Investigation:** Checked Grafana's configured datasource URL and SELinux network-access policy. The recorded resolution identifies the SELinux boolean `grafana_can_tcp_connect_prometheus_port`.

**Root cause:** SELinux policy did not permit the Grafana service domain to make the required outbound TCP connection to Prometheus.

**Corrective action:** Enabled `grafana_can_tcp_connect_prometheus_port` permanently (the recorded resolution used the persistent SELinux boolean, rather than disabling SELinux).

**Validation:** Grafana Explore successfully queried Prometheus.

**Security note:** Keep SELinux enabled and use the narrow supported boolean; do not turn off SELinux to work around application connectivity.

### RCA-005 – Python application failed with ModuleNotFoundError: src

**Symptom:** Running `python src/transaction_insert.py` could raise `ModuleNotFoundError: No module named 'src'`.

**Investigation:** Checked the current working directory and Python package/module import context.

**Root cause:** The file was launched as a standalone script. Its package import expected the project root to be on Python's module search path.

**Corrective action:** Change to `/opt/banking-app`, activate `venv`, and run the module from the project root:
```bash
cd /opt/banking-app
source venv/bin/activate
python -m src.transaction_insert
```

**Validation:** The module-based execution path is the documented working invocation. A separate Python-to-Cassandra connection test was also documented.

### RCA-006 – Custom Cassandra metrics script did not write parsed metrics to the output file

**Symptom:** The first custom metrics collector version printed extracted values in the terminal, but the expected Prometheus textfile did not receive the awk output correctly.

**Investigation:** Reviewed shell redirections in the awk pipeline and the regular expressions matching the `nodetool tablestats` output.

**Root causes:**
- Awk output was displayed but was not appended to the temporary Prometheus metrics file.
- A loose SSTable-count match could include both `SSTable count:` and `Old SSTable count:`.

**Corrective action:**
- Redirected awk output into the temporary metrics file using `>> "$TEMP_FILE"`.
- Anchored the parser patterns so that only the intended `SSTable count:` line matched.
- Omitted `NaN` latency values rather than publishing invalid Prometheus numeric samples.
- Published the finished file by moving the temporary file into place.

**Validation:** The custom metrics file and exporter endpoint showed the table metrics for the three nodes. Prometheus exposed the custom series; `node_textfile_scrape_error` was observed as 0. The metrics collection was manually executed successfully.

**Status boundary:** A one-minute systemd service/timer was proposed, but installation and repeated scheduled execution were not confirmed.

### RCA-007 – Stop script remote verification loop failed

**Symptom:** The project stop script's remote verification loop returned a shell error.

**Investigation:** Reviewed the nested SSH/remote-shell command quoting.

**Root cause:** Nested shell quoting in the remote verification command was incorrect.

**Corrective action / workaround:** Cassandra `drain` and stop commands were executed manually on all three nodes. Prometheus, Grafana and Node Exporter were also stopped. A reference replacement for the lifecycle script was documented, but deployment of a corrected stop script was not confirmed.

**Validation:** The operator was instructed to check the Cassandra JVM process and native port on all three nodes before powering off. Do not treat a failed SSH verification step as proof that a VM or Cassandra process has stopped.

### RCA-008 – Cassandra systemd displayed failed after a controlled stop (exit 143)

**Symptom:** After the stop sequence, `systemctl is-active cassandra` returned `failed`; node 2's service status showed the main Cassandra process ended with status 143 after a successful drain.

**Investigation:** Interpreted the exit status and checked whether a CassandraDaemon JVM or native port remained active.

**Root-cause interpretation:** Exit 143 is consistent with termination by SIGTERM (128 + 15). In this shutdown context, systemd's failed state did not by itself prove a live Cassandra process or an unsuccessful drain.

**Corrective action:** Do not blindly reset the failed unit or power off based only on the service state. Confirm process state with `pgrep -af org.apache.cassandra.service.CassandraDaemon` and listener state with `ss -lntp | grep 9042`.

**Validation:** Use the process/port checks across all three nodes as the shutdown gate. No unsupported claim is made that the systemd unit semantics were permanently changed.

### RCA-009 – LAB3 could not SCP its backup directly to LAB2

**Symptom:** The initial LAB3-to-LAB2 backup transfer failed to authenticate.

**Investigation:** Checked which host held the SSH private key and the direction of the SSH connection.

**Root cause:** LAB3 did not have the private key required to authenticate to LAB2. The key was intentionally not copied to LAB3 and its permissions were not weakened.

**Corrective action:** Used LAB1 as a relay: copied LAB3's snapshot to LAB1 staging, then transferred it from LAB1 to LAB2.

**Validation:** The node3 staging directory was present and its size was checked. The LAB3 source-to-copy SHA-256 comparison was not confirmed, so checksum status remains pending.

### RCA-010 – Snapshot file validation falsely flagged LAB2 components as missing

**Symptom:** A validation command expected a filename beginning with `nb-5-big-` and reported that LAB2 was missing a TOC component.

**Investigation:** Inspected the actual SSTable component names in LAB2's snapshot directory.

**Root cause:** LAB2's SSTables used generation prefix `nb-6-big-`, while LAB1 and LAB3 used `nb-5-big-`. SSTable generation identifiers can differ between nodes; the validator had made an invalid cross-node filename assumption.

**Corrective action:** Changed validation to identify any `*-TOC.txt` component rather than hard-coding the generation prefix. SSTable component files were not renamed.

**Validation:** LAB2's TOC component was found and the copy validation was able to use the actual filename pattern.

### RCA-011 – curl exit 23 after piping exporter output to head

**Symptom:** A command such as `curl .../metrics | head -3` could display `curl: (23)`.

**Root-cause interpretation:** `head` exits after reading the requested lines and closes the pipe; curl may then report a write failure because the reader closed early. This is not, by itself, proof of an exporter outage.

**Corrective action:** Use an output-limiting or discard pattern for availability tests, for example `curl -fsS --max-time 5 http://<ip>:9100/metrics >/dev/null`, and inspect the HTTP response independently.

**Validation:** All three exporter endpoints were separately verified to return metrics.

## Symptoms documented as general troubleshooting guidance, not confirmed RCA incidents

The following appeared in the troubleshooting reference, but the retained evidence does not include a confirmed incident timeline, root cause and completed corrective action for each one:

- Prometheus target DOWN in general.
- CQL connection refused / Cassandra native transport unavailable.
- Cassandra node shown as DN.
- Cassandra authentication failure.
- Generic Python connection/authentication failure.

For these, the runbook directs the DBA to inspect exporter service and target lastError, Cassandra port 9042, systemd and Cassandra logs, network/gossip, and authentication configuration. Do not present these generic examples as successfully resolved production incidents.

## Open RCA / engineering findings

### RCA-012 – Commit Log archive script no-overwrite race

**Finding:** Version 2.0 checks whether the destination exists and subsequently uses `mv`. Another process could create the same destination between the check and move, so the move could overwrite an archive file that appeared during that interval.

**Status:** Identified by code review, not a reported real-segment data-loss incident.

**Next action:** Implement a race-safe no-clobber publication method and test fresh-copy, identical duplicate, conflicting duplicate and concurrent-write cases with dummy files only.

### RCA-013 – Archive failure/retry semantics not yet signed off

**Finding:** The Cassandra 4.1.12 archive callback contract, error behaviour and retry/reconciliation semantics still require version-specific implementation review.

**Status:** Open. Do not enable live archiving.

**Next action:** Verify against Cassandra 4.1.12 implementation/docs; design monitoring, failed-segment detection and a reconciliation process.

## Standard evidence to attach to future RCA entries

- Exact command and unedited error output (with secrets redacted).
- Timestamp, VM/node and scope.
- Relevant service status, listener, firewall or SELinux output.
- Relevant Cassandra, Prometheus, Grafana or application log excerpt.
- Root cause and why alternative hypotheses were ruled out.
- Change performed, rollback plan and before/after result.
- Performance or availability impact, where measured.


### RCA-014 – cqlsh to localhost failed while private IP worked

**Symptom:** The retained project guide records that cqlsh to 127.0.0.1 failed while cqlsh to the node's private IP worked.

**Investigation / guidance recorded:** Use the verified node IP and inspect Cassandra `rpc_address` and native transport configuration if needed.

**Root cause:** The exact `rpc_address` value and full error output were not retained. A precise bind-address root cause is therefore not asserted.

**Workaround and validation:** Use `cqlsh 192.168.62.134 9042`; the private-IP connection succeeded.

**Status:** Connection workaround verified. Root cause is only partially established because the original listener/configuration evidence is unavailable.
