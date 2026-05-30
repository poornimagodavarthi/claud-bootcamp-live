---
name: security-checklist
description: Run a security review on a project or diff against the OWASP Top 10 and rank findings by exploitability.
---

## Purpose

Checks a file, diff, or project against the OWASP Top 10 vulnerability
categories and surfaces concrete, exploitable findings with severity
ratings and minimal remediation steps.

## When to use it

- Before shipping any code that handles user input, authentication, or external data.
- After an AI tool generates route handlers, parsers, or data models.
- As a pre-merge gate for changes that touch auth, sessions, or SQL queries.
- When a dependency is updated and its attack surface may have changed.

## Prompt body

```text
Run a security review on TARGET against the OWASP Top 10 (2021 edition).

TARGET: TARGET (file path, diff, or `--staged`)

Check each category below. For each finding, state:
- OWASP category and ID (e.g. A03 Injection)
- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Exact location (file:line)
- One sentence describing the risk
- The smallest code change that closes it

Categories to check (in order):
A01 Broken Access Control
A02 Cryptographic Failures
A03 Injection (SQL, command, LDAP, XPath)
A04 Insecure Design
A05 Security Misconfiguration
A06 Vulnerable and Outdated Components
A07 Identification and Authentication Failures
A08 Software and Data Integrity Failures
A09 Security Logging and Monitoring Failures
A10 Server-Side Request Forgery

If no issues are found in a category, skip it.
Sort output: CRITICAL first, then HIGH, MEDIUM, LOW.
End with a one-line summary: "N finding(s): X critical, Y high, Z medium, W low."
```

## Expected inputs

- `TARGET` — a file path, `--staged` for the current git diff, or a pasted code block.

## Expected outputs

- Findings grouped by severity (CRITICAL → HIGH → MEDIUM → LOW).
- Each finding: OWASP category, location, risk sentence, minimal fix.
- A one-line summary count at the end.

## Worked example

**Scenario:** Security review of a notes API route file.

**Invocation:**
```
/security-checklist TARGET=api/routes/notes.py
```

**Expected output (excerpt):**
```
A03 Injection — MEDIUM — api/routes/notes.py:31
User-supplied `q` is embedded in a LIKE pattern without escaping `%` and `_`,
allowing wildcard injection that returns unintended rows.
Fix: escape metacharacters in `q` before building the pattern.

A09 Security Logging — LOW — api/routes/notes.py (global)
No request logging or error logging is present; failed auth or 500 errors
are invisible to operators.
Fix: add structured logging at the route level for 4xx and 5xx responses.

2 finding(s): 0 critical, 0 high, 1 medium, 1 low.
```
