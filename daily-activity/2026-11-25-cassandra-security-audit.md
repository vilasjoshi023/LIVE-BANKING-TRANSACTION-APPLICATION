# 25 November 2026 – Cassandra Security Audit and Authentication Readiness

## Objective

Perform a read-only security assessment of the three-node VJCLAB Cassandra cluster, validate the current authentication/authorization, TLS, JMX, firewall, SSH and audit-logging posture, prepare the authentication metadata for a controlled rollout, and identify Python application dependencies.

This is a learning lab using synthetic banking data. It is not a production banking service.

## Environment

- Cluster: VJCLAB, Apache Cassandra 4.1.12.
- Datacenter/rack: dc1 / rack1.
- Nodes:
  - VJC9LAB1 – 192.168.62.134
  - VJC9LAB2 – 192.168.62.135
  - VJC9LAB3 – 192.168.62.136
- Workload host/application root: LAB1, /opt/banking-app.
- Keyspace/table reviewed: banking_stream.bank_transactions.
- Cassandra configuration: /opt/cassandra/conf/cassandra.yaml.
- JMX local port: 7199; native transport port: 9042; internode port: 7000; JMX Exporter port: 9404; Node Exporter port: 9100; Prometheus port: 9090.

## 1. Cassandra authentication and authorization baseline

Inspected the four role/security settings on each node. All three nodes returned the same configuration:

| Setting | Value on all nodes | Assessment |
|---|---|---|
| authenticator | AllowAllAuthenticator | Client authentication is not required |
| authorizer | AllowAllAuthorizer | Normal Cassandra permission enforcement is disabled |
| role_manager | CassandraRoleManager | Cassandra role manager is configured |
| network_authorizer | AllowAllNetworkAuthorizer | Role-based network authorization is not enforced |

Connected to LAB1 without supplying credentials using the cqlsh executable under /opt/cassandra/bin.

Observed behavior:
- LIST ROLES returned an Unauthorized error because the session was anonymous and role-management operations require an authenticated identity.
- DESCRIBE TABLE banking_stream.bank_transactions succeeded.
- A bounded SELECT of five transaction IDs for the partition date 2026-11-18 succeeded without credentials.
- SELECT role, can_login, is_superuser, member_of FROM system_auth.roles returned the cassandra role with can_login=true and is_superuser=true.
- A subsequent SELECT * from system_auth.roles returned the salted_hash column. The sensitive value is deliberately not reproduced in this repository. Treat this exposure as a credential-material disclosure and rotate the affected credential as part of the controlled authentication rollout. Do not query, publish or manually edit salted_hash.

Finding SEC-01: Anonymous CQL access is accepted.
Finding SEC-02: Cassandra authorization enforcement is disabled.
Finding SEC-11: Anonymous access exposed password-hash material stored in system_auth. The hash value is intentionally excluded from this record.

The successful table read demonstrates that a client able to reach the native transport endpoint can read application data under the current configuration. Actual reachability is still constrained by host and network firewalls; this lab test does not establish internet exposure.

## 2. system_auth replication strategy change

Initial metadata showed system_auth using SimpleStrategy with replication_factor=3.

Before enabling authentication, changed the keyspace replication strategy to NetworkTopologyStrategy while retaining three replicas in dc1:

~~~sql
ALTER KEYSPACE system_auth
WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'dc1': 3
};
~~~

Post-change evidence:
- nodetool describecluster listed system_auth as NetworkTopologyStrategy {dc1=3}.
- All three nodes were live; joining, moving, leaving and unreachable counts were zero.
- All three nodes reported the same schema version UUID: 98445228-c09a-3c64-9e53-273e8918b325.
- Datacenter dc1 contained three nodes.
- nodetool status showed all three nodes UN.
- nodetool compactionstats reported pending tasks: 0.

The previous SimpleStrategy RF=3 and resulting NetworkTopologyStrategy dc1=3 both select all three nodes in this single-datacenter, three-node lab. The strategy change did not change the replica count. No repair was run solely for this strategy change.

Topology limitation: all three nodes are configured in rack1. NetworkTopologyStrategy is appropriate for datacenter-aware production topology, but this lab does not demonstrate rack-level failure isolation.

## 3. system_auth table inspection

Used nodetool tablestats system_auth on LAB1.

Observed on LAB1:
- roles: one SSTable, approximately 5,182 bytes live/on disk, four local reads, zero writes in the displayed statistics.
- role_permissions, role_members, network_permissions and resource_role_permissons_index: zero SSTables and zero recorded local reads/writes in the displayed statistics.
- Pending flushes: zero.

The tablestats values are node-local observations, not a cluster-wide audit of all table data.

At the initial anonymous-access baseline, the role inventory contained only the cassandra role. Subsequent authenticated pilot work created separate DBA, banking application and reporting roles; see the authentication pilot section below.

## 4. Pre-authentication snapshot

Created the named system_auth snapshot on all three nodes:

~~~bash
/opt/cassandra/bin/nodetool snapshot -t pre_auth_security_20261125 system_auth
~~~

Snapshot verification with nodetool listsnapshots confirmed five system_auth tables on each node:
- roles
- role_permissions
- role_members
- network_permissions
- resource_role_permissons_index

The roles snapshot showed 88 bytes true size and approximately 5.06–5.15 KiB disk usage per node. Snapshot creation times were approximately 15:00 UTC on 25 November 2026.

Security handling:
- The snapshot includes authentication metadata and must be treated as sensitive.
- Restrict filesystem access to Cassandra administrators.
- Do not publish snapshot files or copy them to an unencrypted location.
- These are node-local snapshots, not an independent off-host backup.

## 5. Client and internode TLS baseline

Inspected encryption configuration on all three nodes.

| Setting | Observed value |
|---|---|
| client_encryption_options.enabled | false |
| server_encryption_options.internode_encryption | none |
| server_encryption_options.require_client_auth | false |
| server_encryption_options.require_endpoint_verification | false |

The configuration is consistent across LAB1, LAB2 and LAB3.

Finding SEC-03: Client-to-node TLS is disabled.
Finding SEC-04: Internode encryption is disabled.

The configured listen_address and rpc_address values are node-specific private addresses:
- LAB1: 192.168.62.134
- LAB2: 192.168.62.135
- LAB3: 192.168.62.136

The native transport port is 9042. The internode listener is on port 7000. No listener on port 7001 was shown in the captured socket output.

## 6. JMX and exporter listener review

Socket inspection on all three nodes showed:
- Cassandra JMX 7199 bound to 127.0.0.1 only.
- Cassandra internode 7000 bound to each node's private address.
- CQL 9042 bound to each node's private address.
- JMX Exporter 9404 listening on 0.0.0.0 on all three nodes.
- Node Exporter 9100 listening on each node's private address.
- Prometheus 9090 listening on LAB1's private address.

The Cassandra environment file showed LOCAL_JMX=yes on all nodes. In this local-JMX mode, JMX remote authentication is configured as false, but the captured socket binding is loopback-only. Do not infer that JMX is remotely exposed from the authentication flag alone.

Finding SEC-07: Cassandra JMX is restricted to localhost by its observed listener binding. Continue to restrict local operating-system access.

Finding SEC-09: JMX Exporter listens on all interfaces. LAB2 and LAB3 displayed firewalld rich rules permitting port 9404 from LAB1 (192.168.62.134/32). LAB1's displayed rules did not show a matching 9404 rich-rule exception. Wildcard binding does not by itself establish external reachability; confirm effective firewall and network paths before drawing that conclusion.

## 7. Firewalld and administrative service review

All three hosts showed firewalld running with the public zone active on ens33.

The displayed firewall rules included source-specific allowlists for Cassandra ports 7000 and 9042 between the cluster nodes. Monitoring exceptions included LAB1 as the source for selected Node Exporter and JMX Exporter ports on LAB2/LAB3.

The active zone listed services:
- cockpit
- dhcpv6-client
- ssh

The SSH service query returned yes on all nodes. The port 9404/tcp direct port query returned no; source-specific rich rules were present for LAB2 and LAB3.

Cockpit socket status was inactive on all three nodes.

Finding SEC-05: Cassandra port allowlists are present, but full reachability validation and review of all monitoring endpoints remain pending.
Finding SEC-08: SSH is enabled in the public zone; source restrictions were not shown in the displayed rich rules.
Positive control: Cockpit socket was inactive.

## 8. SSH configuration review

Effective sshd settings were identical across the nodes:

| Setting | Value |
|---|---|
| permitrootlogin | without-password |
| passwordauthentication | yes |
| pubkeyauthentication | yes |
| maxauthtries | 6 |
| authenticationmethods | any |

SSH listened on 0.0.0.0:22 and [::]:22 on all nodes.

Interpretation:
- Root password login is prohibited by the observed PermitRootLogin setting, but root key-based login is allowed.
- Password authentication remains enabled for eligible non-root accounts.
- SSH is listening on IPv4 and IPv6 wildcard addresses.
- Firewalld permits the SSH service in the active public zone.

Finding SEC-08: SSH source restriction and password-authentication hardening require review. Do not disable password authentication until administrator key access and recovery access have been validated.

## 9. Cassandra audit logging

All nodes showed:

~~~yaml
audit_logging_options:
  enabled: false
  logger:
    - class_name: BinAuditLogger
~~~

The logger class is configured but audit logging is disabled.

Finding SEC-06: Cassandra built-in audit logging is disabled. Audit categories, audit log path, retention, rotation, archive handling and disk-capacity impact remain to be designed before enabling it.

## 10. Application dependency inventory and scheduled monitoring

Identified the following Python modules referencing the central Cassandra connection factory or session:
- /opt/banking-app/src/cassandra_connection.py
- /opt/banking-app/src/transaction_insert.py
- /opt/banking-app/src/transaction_concurrent_test.py
- /opt/banking-app/src/slow_query_lab.py

The central connection factory was reviewed and enhanced with optional PlainTextAuthProvider support. The updated module was syntax-checked and tested against the still-anonymous Cassandra cluster; it connected successfully and retained LOCAL_QUORUM. No username/password variables were configured during this preparation test. The .env file permission was changed to 0600 (root:root), and a pre-authentication copy of cassandra_connection.py was retained. No .env values or credentials were collected or committed.

The systemd service inventory showed banking-slow-query.service as a static unit, along with cassandra-prometheus-metrics.service and cassandra.service.

Subsequent timer verification on LAB1 showed:
- systemctl is-enabled banking-slow-query.timer: enabled
- systemctl is-active banking-slow-query.timer: active
- At the time of capture, last scheduled activation was Wed 25 Nov 2026 20:31:55 IST and next activation was Wed 25 Nov 2026 20:37:00 IST.
- The timer is configured for approximately five-minute recurring execution.

This confirms that the timer is enabled and active. Multiple successive timer-triggered workload successes and metric refreshes were not yet verified in the captured evidence.

## 11. Findings register

| ID | Control | Evidence / status | Initial priority |
|---|---|---|---|
| SEC-01 | Cassandra authentication | AllowAllAuthenticator; anonymous table read succeeded | High |
| SEC-02 | Cassandra authorization | AllowAllAuthorizer | High |
| SEC-03 | Client TLS | client encryption disabled | High |
| SEC-04 | Internode TLS | internode_encryption none | High |
| SEC-05 | Network exposure | Source-specific Cassandra allowlists present; full reachability validation pending | Medium |
| SEC-06 | Audit logging | audit_logging_options enabled=false | Medium |
| SEC-07 | JMX | 7199 bound to 127.0.0.1 on all nodes | Positive control |
| SEC-08 | SSH | Public-zone SSH; password authentication enabled; wildcard listener | High |
| SEC-09 | JMX Exporter | 9404 wildcard listener; source-specific rules shown on LAB2/LAB3 | Medium |
| SEC-10 | Cockpit | cockpit.socket inactive | Positive control |
| SEC-11 | Authentication metadata | Anonymous query returned salted_hash material; raw value excluded | High |

Priorities are preliminary lab remediation priorities, not a formal compliance rating or external audit certification.

## 12. Work completed and not completed

Completed:
- Read-only authentication, authorization, TLS, JMX, firewall, SSH and audit-logging review across all three Cassandra nodes.
- Confirmed anonymous access to banking_stream.bank_transactions from LAB1.
- Confirmed current role inventory contains only cassandra, with can_login and is_superuser true.
- Changed system_auth replication from SimpleStrategy RF=3 to NetworkTopologyStrategy dc1=3.
- Verified matching schema version and three live nodes after the change.
- Captured and verified pre_auth_security_20261125 snapshots on all three nodes.
- Identified Python application modules and confirmed banking-slow-query.timer is enabled and active.

Not completed:
- Cassandra connection factory source review and credential-injection design.
- Verification of banking_app and banking_readonly access restrictions (both role logins later succeeded; least-privilege enforcement remains pending because CassandraAuthorizer is not enabled).
- PasswordAuthenticator rollout to LAB1 and LAB2; LAB3 pilot only is complete.
- CassandraAuthorizer rollout and least-privilege grants.
- Default superuser credential rotation and retirement.
- Client TLS and internode TLS rollout.
- Audit logging enablement and retention design.
- SSH and monitoring endpoint hardening.
- Verification of multiple successful timer-triggered runs after activation.

## 13. Safe next steps

1. Review /opt/banking-app/src/cassandra_connection.py without displaying or committing .env values or secrets.
2. Identify all client processes and units that connect to Cassandra, including the slow-query timer service.
3. Design the role hierarchy and minimum permissions for banking_stream.
4. Confirm administrative recovery access, certificate plan and maintenance/rollback procedure.
5. Stage authentication changes using the Cassandra 4.1 documented procedure; validate application and monitoring clients before proceeding to authorization enforcement.
6. Plan client and internode TLS separately and validate certificates/trust before rollout.
7. Design audit logging filters, storage, rotation and retention before enabling it.
8. Validate effective firewalld access paths and restrict SSH/metrics access to intended management sources.

The initial read-only assessment did not change authenticator/authorizer settings. Subsequent staged authentication work changed authenticator to PasswordAuthenticator on LAB3 only and restarted that node; an authenticated cqlsh session to LAB3 succeeded. LAB1 and LAB2 remain on AllowAllAuthenticator. All three nodes still use AllowAllAuthorizer; authorization has not been enabled. No TLS, audit-logging, SSH or firewall changes were made. The system_auth replication-strategy update and the LAB3 authentication pilot are the Cassandra configuration changes performed to date.

## 14. Follow-up implementation – authentication pilot and Python client preparation

This section records work completed after the initial read-only audit on 25 November 2026. It supersedes any earlier statements in this document that describe role creation or the authentication rollout as wholly pending.

### Python connection factory preparation

Reviewed /opt/banking-app/src/cassandra_connection.py. The original factory:
- Loaded /opt/banking-app/config/.env.
- Used three contact points, native transport port 9042, local DC dc1 and keyspace banking_stream.
- Used DCAwareRoundRobinPolicy and set LOCAL_QUORUM.
- Did not configure a Cassandra authentication provider.

Confirmed that transaction_insert.py, transaction_concurrent_test.py and slow_query_lab.py all call the shared get_cassandra_session() factory.

Security preparation:
- Created src/cassandra_connection.py.bak.pre_auth_20261125 before replacing the source.
- Changed /opt/banking-app/config/.env permissions from 0644 to 0600, owner root:root.
- Enhanced cassandra_connection.py with optional PlainTextAuthProvider support using CASSANDRA_USERNAME and CASSANDRA_PASSWORD.
- Added validation requiring the username and password to be configured together, plus required connection-setting validation.
- Preserved the three contact points, port 9042, dc1 load balancing, banking_stream keyspace and LOCAL_QUORUM consistency.
- Syntax validation passed.
- The configuration diagnostic reported three contact points, port 9042, dc1, banking_stream and authentication provider not configured.
- A connection test successfully connected to cluster VJCLAB, keyspace banking_stream, and printed consistency value 6 (LOCAL_QUORUM). This test used the still-anonymous configuration and did not validate credential authentication.

No .env contents, passwords, tokens or credential values are stored in this repository.

### Authentication pilot on LAB3

- Backed up /opt/cassandra/conf/cassandra.yaml on LAB3 to cassandra.yaml.pre_auth_20261125.
- Changed only LAB3's authenticator from AllowAllAuthenticator to PasswordAuthenticator.
- Restarted LAB3's Cassandra service.
- Successfully connected to 192.168.62.136:9042 using the cassandra username and the password entered at the interactive prompt.
- LIST ROLES succeeded in the authenticated session.
- The Non-system keyspaces don't have the same replication settings, effective ownership information is meaningless message was observed with nodetool status/metadata output. It is an informational ownership-calculation warning due to differing keyspace replication configurations, not evidence of a node being down.

### Roles created on LAB3 using authenticated DBA access

The authenticated dba_admin session returned the following role inventory:

| Role | Login | Superuser | Intended responsibility |
|---|---|---|---|
| cassandra | true | true | Default superuser; temporary during migration |
| dba_admin | true | true | Replacement DBA administration |
| banking_app | true | false | Banking application runtime |
| banking_readonly | true | false | Read-only/reporting client |

The successful prompt dba_admin@cqlsh and subsequent LIST ROLES output verify that the dba_admin account authenticated successfully. The LIST ROLES output confirms that banking_app and banking_readonly exist with login enabled and superuser disabled. Their separate password-login tests subsequently succeeded on LAB3; see section 15. Authorization restrictions remain untested.

No role was created with a superuser grant for the application or reporting roles.

### Current per-node state after the pilot

The latest captured configuration comparison showed:

| Node | authenticator | authorizer | Current state |
|---|---|---|---|
| VJC9LAB1 | AllowAllAuthenticator | AllowAllAuthorizer | Not migrated |
| VJC9LAB2 | AllowAllAuthenticator | AllowAllAuthorizer | Not migrated |
| VJC9LAB3 | PasswordAuthenticator | AllowAllAuthorizer | Authentication pilot |

This is a mixed-authenticator transition state. LAB3 requires credentials, while LAB1 and LAB2 still accept anonymous connections. The cluster is not yet fully secured.

Cassandra authorization is not yet enabled on any node. CassandraAuthorizer has not been configured; no least-privilege grants have been applied; and the current banking_app/banking_readonly role names do not yet enforce different permissions while AllowAllAuthorizer remains active.

### Scheduled workload coordination

Before further node authentication/authorization restarts, the operator was instructed to pause banking-slow-query.timer and verify that banking-slow-query.service was inactive. A stop command was issued, but no post-stop status output has yet been recorded in the audit evidence. Therefore the current timer state is marked unverified pending a fresh systemctl is-active and systemctl list-timers check.

### Current completion status

Completed:
- Python connection factory enhanced with optional authentication support and validated against the anonymous pilot-compatible state.
- .env permission hardened to 0600.
- LAB3 PasswordAuthenticator pilot configured and tested with an authenticated cqlsh login.
- Replacement dba_admin login verified.
- banking_app and banking_readonly role records created and visible in LIST ROLES.
- LAB1/LAB2 configuration comparison confirms they have not yet migrated to PasswordAuthenticator.

Pending:
- Verify least-privilege allowed/denied operations for banking_app and banking_readonly after CassandraAuthorizer is enabled.
- Verify the current state of the slow-query timer and service before further maintenance.
- Review whether application credentials should be held in a root-only environment file or a dedicated secret-management mechanism; do not populate credentials until client TLS is in place or an explicitly approved protected test path is defined.
- Enable CassandraAuthorizer only after preparing and testing the required permissions and rollout/rollback plan.
- Grant only the permissions required by each application role and test allowed/denied operations.
- Roll out authentication and then authorization to LAB1 and LAB2 using the Cassandra 4.1 documented rolling procedure.
- Rotate/retire the default cassandra superuser only after replacement DBA access is validated on the full cluster.
- Validate every scheduled/application client after authentication and authorization enforcement.

No authorization, TLS, audit-logging, SSH or firewall changes have been made. The application-role logins and cross-node authenticated operation remain unverified.


## 15. Latest pilot validation checkpoint – 25 November 2026

The following results were captured after creating the DBA and application roles:

### Application login tests on LAB3

- Connected to VJC9LAB3 (192.168.62.136) as `banking_app` using an interactive password prompt. Login succeeded.
- Executed a bounded SELECT against `banking_stream.bank_transactions` for partition date `2026-11-18` with `LIMIT 1`. One row was returned.
- Connected to VJC9LAB3 as `banking_readonly` using its separate interactive password prompt. Login succeeded.
- Executed the same bounded SELECT; the same one-row result was returned.
- These tests validate the role credentials and CQL connectivity on LAB3. They do **not** validate read-only access control because the authorizer remains `AllowAllAuthorizer`.

### Maintenance and cluster status

- `systemctl is-active banking-slow-query.timer` returned `inactive`.
- `systemctl is-active banking-slow-query.service` returned `inactive`.
- `nodetool status` from LAB1 showed VJC9LAB1, VJC9LAB3 and VJC9LAB2 all in `UN` state in dc1.
- The output included the previously observed note that effective ownership is meaningless when non-system keyspaces use different replication settings. This is an ownership-calculation warning, not a node-down indication.
- The requested `nodetool clientstats` output from LAB3 was not included in the latest evidence. Client-connection inventory is therefore still pending.

### Authorization rollout status

The latest node configuration comparison remains:

| Node | authenticator | authorizer |
|---|---|---|
| VJC9LAB1 | AllowAllAuthenticator | AllowAllAuthorizer |
| VJC9LAB2 | AllowAllAuthenticator | AllowAllAuthorizer |
| VJC9LAB3 | PasswordAuthenticator | AllowAllAuthorizer |

No authorizer change to `CassandraAuthorizer` has been performed. The next authorization pilot is blocked pending LAB3 `nodetool clientstats` review and a final confirmation that no client workload is using LAB3. The DBA account and both application role logins are now verified on LAB3; authorization grants and allowed/denied-operation tests remain pending.

### Current action boundary

- Do not disable the default `cassandra` superuser yet.
- Do not enable `CassandraAuthorizer` until required grants and the pilot-node client inventory are reviewed.
- Keep the slow-query timer paused during the next maintenance/restart step.
- No TLS, audit logging, SSH or firewall changes have been applied.
