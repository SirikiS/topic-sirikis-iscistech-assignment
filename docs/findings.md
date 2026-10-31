# Security findings and prioritisation

| Finding | Source | Severity | Business impact | Starter code or new feature |
| --- | --- | --- | --- | --- |
| SQL injection in scan search logic | Manual review and parameterized fix | Critical | Attackers can alter or exfiltrate scan records by injecting wildcards or UNION payloads in the search query. | Starter code |
| Hardcoded secrets and service keys in configuration | Manual review and config audit | Critical | Compromise of a single configuration file or source repository gives attackers reusable credentials and JWT signing material. | Starter code |
| JWT verification accepts the `none` algorithm | Manual review of `auth.py` | Critical | A malicious client can forge tokens with an unsigned payload and bypass authentication. | Starter code |
| Passwords and secrets are logged in plaintext | Manual review of login logging | High | Security logs may expose access credentials and increase the blast radius of a log leak. | Starter code |
| Overly permissive CORS and credentialed wildcard access | Manual review | High | Browser-based attacks can read authenticated API responses if untrusted origins are allowed. | Starter code |
| Sensitive error traces returned to clients | Manual review of exception handler | Medium | Stack traces reveal internal paths and library versions that simplify exploitation. | Starter code |
| Public share links are not time-limited or password-protected by default | Task 1 implementation review | High | External recipients can retain or replay a valid link beyond the intended use. | New feature |

## Priority summary

The most urgent issues were the authentication bypass, raw SQL injection, and embedded credentials. These risks directly undermine the integrity of the application and would allow both unauthorised access and data theft. The share feature was implemented with token hashing, expiry, and optional password checks to ensure the new capability did not recreate the same risk pattern.
