# Redis Key Schema — Layer 4 Documentation for Ashish

## Key Naming Convention
All keys follow: `zt:{category}:{identifier}`

## Keys

| Key Pattern | Type | TTL | Purpose |
|---|---|---|---|
| `zt:session:{token}` | Hash | 3600s (1hr) | Cached session data: user_id, risk_score, decision |
| `zt:failed:{user_id}` | Integer | 900s (15min) | Failed login attempt counter per user |
| `zt:failed:ip:{ip_hash}` | Integer | 900s (15min) | Failed login counter per IP |
| `zt:ratelimit:{user_id}` | Integer | 60s | Request count for token bucket (per user) |
| `zt:ratelimit:ip:{ip_hash}` | Integer | 60s | Request count for token bucket (per IP) |
| `zt:mfa_pending:{session_token}` | String | 300s (5min) | Marks session as awaiting MFA completion |

## Usage Notes for Ashish
- Increment `zt:failed:{user_id}` on every failed login. Reset on success.
- Read `zt:session:{token}` first on every request — if hit, skip DB query.
- Write to `zt:session:{token}` after every risk re-evaluation.
- If `zt:mfa_pending:{token}` exists, block all non-MFA routes.