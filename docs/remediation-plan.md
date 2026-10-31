# Remediation plan and residual risk

## Fixed in this change set

1. Replaced raw SQL concatenation with bound parameters in `app/database.py`.
2. Restricted JWT verification to the configured algorithm in `app/auth.py`.
3. Removed raw password logging and reduced exception leakage in `app/main.py`.
4. Moved secret defaults into environment variables and documented secret-managed values in the deployment chart.
5. Added time-bounded, hashed share tokens with optional password gating in `app/main.py` and `app/models.py`.

## Residual risk and deferred items

| Residual risk | Why not fully remediated | Effort | Compensating controls |
| --- | --- | --- | --- |
| Full secret rotation and key management | Requires integration with a real secret store and coordinated rotation across running environments | Medium | Use workload identity or a managed secret manager in deployment; rotate JWT signing keys on schedule |
| Cross-origin browser protections for all clients | A production API may need a stricter allowlist based on deployed frontend domains | Low | Restrict allowed origins via environment configuration and reject untrusted hosts |
| Fine-grained authorization for shared links | Share tokens are currently scoped to a single scan and owner; multi-user delegated access would need a more complex policy model | Medium | Use explicit ownership checks and audit logging for share creation |

This is a practical risk profile for a small internal service: critical integrity issues were closed immediately, while longer-term governance tasks remain for production hardening.
