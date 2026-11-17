# Module 01 – Linux, Storage and Networking for DBAs

## Learning objective
Understand the operating system underneath Cassandra well enough to distinguish application, database, OS, storage and network symptoms.

## A. Beginner topics
- Computer/VM basics: CPU, vCPU, cores, RAM, swap, virtual disk, NIC, hypervisor and resource contention.
- Linux directory tree: /etc, /var, /var/log, /opt, /usr, /home, /tmp, /proc and /sys.
- File commands: pwd, ls, cd, mkdir, touch, cp, mv, rm, find, file, stat, du, df.
- Text commands: cat, less, head, tail, grep, cut, sort, uniq, wc, awk and sed.
- Permissions: owner/group/other, rwx, chmod, chown, umask, sudo, ACLs and service users.
- Process commands: ps, top, free, uptime, pgrep, kill, lsof, ss and journalctl.
- systemd basics: start, stop, restart, reload, enable, disable, status, unit files and journals.

## B. Networking topics
- IPv4 address, subnet/CIDR, gateway, DNS, routing table, ARP, TCP/UDP and loopback.
- TCP listener vs outbound client, bind address, firewall filtering, connection refused vs timeout vs no route.
- Cassandra ports in this lab: 7000 internode, 9042 native transport, 7199 local JMX, 9404 JMX Exporter, 9100 Node Exporter, 9090 Prometheus, 3000 Grafana.
- firewalld zones, services, rich rules and source restriction.
- SELinux enforcing mode, contexts, booleans and audit denials.
- MTU, latency, packet loss, retransmits, DNS and TLS basics.

## C. Storage topics
- Disk, partition, LVM PV/VG/LV, filesystem, mount, inode, hard link and soft link.
- Capacity vs throughput vs IOPS vs latency.
- Filesystem fullness, inode exhaustion, disk queue and write cache.
- Cassandra data, commitlog, hints and backup paths; keep them separate and understand their storage pressure.
- Do not manually manipulate live Cassandra data files.

## D. Practical lab – inventory all VMs
Run on each node:
```bash
hostname
hostname -I
uptime
lscpu
free -h
swapon --show
lsblk -f
df -hT
df -ih
ip -br addr
ip route
```
Expected: identify each lab hostname/IP, available memory, swap, filesystem and network interface. Record differences; do not copy one VM's values to another.

## E. Practical lab – process and service inspection
```bash
ps -ef | grep -i cassandra
pgrep -af CassandraDaemon
systemctl status cassandra --no-pager
journalctl -u cassandra -n 100 --no-pager
ss -lntp
```
Explain the difference between a systemd unit state, JVM process state and listening TCP socket. A unit marked failed after process termination does not by itself prove the JVM is still running.

## F. Practical lab – port reachability RCA
For one known service, inspect listener, host firewall and remote reachability:
```bash
sudo ss -lntp
sudo firewall-cmd --state
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --list-all
curl -v --connect-timeout 3 http://192.168.62.134:9100/metrics
```
Interpret:
- Connection refused: path reached a host but no service accepted the connection or a reject rule intervened.
- Timeout: packet/service response not received in time.
- No route to host: route or an intermediate/host firewall reject may be involved.
- HTTP 302 from Grafana may be a normal login redirect.
Never disable firewalld as a troubleshooting shortcut.

## G. Practical lab – Linux RCA mini-cases
1. Disk 100%: inspect df -hT, df -ih, du -xhd1, lsof +L1; identify owner before cleanup.
2. Memory pressure: inspect free -h, vmstat, top, process RSS and swap; do not randomly kill Cassandra.
3. Port not listening: inspect systemd, process, logs and bind address.
4. Permission denied: inspect namei -l, stat, getfacl and SELinux audit records.
5. SELinux denial: inspect ausearch/sealert if installed; find supported boolean/label fix without disabling SELinux.

## H. DBA automation
- Bash variables, arrays, quoting, exit status, pipes, redirection, functions, getopts, traps and temporary files.
- Cron vs systemd timer; service dependencies, timeout, locking, logs and monitoring.
- Log rotation, safe cleanup, idempotency and rollback.
- Shell linting and negative tests.

## Completion gate
Produce a versioned three-node Linux inventory, network/port map, service/process verification checklist and two evidence-backed RCAs. Mark this module Complete only after practical outputs are reviewed.
