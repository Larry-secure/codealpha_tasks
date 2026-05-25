# Secure Coding Review - CodeAlpha Internship

**Application:** SecureBank Web App  
**Language:** Python (Flask)  
**Reviewer:** Ayinde Olaoluwa Joshua  
**Date:** May 2026

---

## Finding 1: SQL Injection

| Field | Details |
|-------|---------|
| **Location** | Login, Search, Register functions |
| **Severity** | Critical |
| **Description** | User input directly concatenated into SQL queries |
| **Impact** | Authentication bypass, data theft, database compromise |
| **Proof** | Username: `admin'--` bypasses login |
| **Fix** | Use parameterized queries |

---

## Finding 2: Cross-Site Scripting (XSS)

| Field | Details |
|-------|---------|
| **Location** | Profile page (`msg` parameter) |
| **Severity** | High |
| **Description** | User input rendered in HTML without escaping |
| **Impact** | Session hijacking, malware injection |
| **Proof** | `/profile?msg=&lt;script&gt;alert('XSS')&lt;/script&gt;` |
| **Fix** | Escape all output with `markupsafe.escape()` |

---

## Finding 3: Hardcoded Secret Key

| Field | Details |
|-------|---------|
| **Location** | `app.secret_key` configuration |
| **Severity** | High |
| **Description** | Secret key hardcoded in source code |
| **Impact** | Session forgery, account takeover |
| **Fix** | Load from environment variable |

---

## Finding 4: Plaintext Password Storage

| Field | Details |
|-------|---------|
| **Location** | Database, Registration |
| **Severity** | Critical |
| **Description** | Passwords stored without hashing |
| **Impact** | Immediate credential exposure if database leaked |
| **Fix** | Use bcrypt hashing |

---

## Finding 5: Debug Mode Enabled

| Field | Details |
|-------|---------|
| **Location** | `app.run(debug=True)` |
| **Severity** | Medium |
| **Description** | Debug mode exposes stack traces and interactive console |
| **Impact** | Source code leak, remote code execution |
| **Fix** | Set `debug=False` in production |

---

## Recommendations

1. Use parameterized queries for all database operations
2. Escape all user input before rendering in HTML
3. Store secrets in environment variables
4. Hash passwords with bcrypt or Argon2
5. Disable debug mode for production
6. Implement input validation and rate limiting
