# Section 10 – Security and Access Control

**Master Program source section:** 10  
**Tracking status:** In progress. LAB3 authentication and role logins validated; authorizer remains AllowAllAuthorizer. LAB3 clientstats output remains outstanding.

## Source syllabus topics

- Authentication & RBAC
- Roles & permissions
- TLS encryption
- Audit logging
- Security best practices

## Learning objective

Implement authenticated client access and least-privilege authorization with safe rollout, certificates and audit controls.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Review the security audit and mixed state: LAB3 PasswordAuthenticator; LAB1/LAB2 AllowAllAuthenticator.
2. Confirm dba_admin, banking_app and banking_readonly logins on LAB3; distinguish authentication tests from permission enforcement.
3. Review LAB3 nodetool clientstats and verify no application client is using the node before the authorizer pilot.
4. Plan CassandraAuthorizer and required grants before enforcement; test permitted and denied operations in the pilot.
5. Plan client/internode TLS separately; design audit-log destination, retention and disk budget.
6. Keep the default cassandra superuser until replacement DBA access is validated across the cluster.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Per-node security configuration comparison.
- [ ] Role/permission matrix and successful/denied operation tests.
- [ ] TLS and audit logging implementation/rollback plan.

## Interview checkpoint

- What is authentication versus authorization?
- Why does CassandraAuthorizer require explicit grants?
- Why plan TLS before sending application passwords over the network?

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
