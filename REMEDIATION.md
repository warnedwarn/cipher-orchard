# Steward remediation

| Mandatory requirement | Code path | Targeted proof | Deployment proof | Status |
| --- | --- | --- | --- | --- |
| Reject a duplicate graft even when its first attempt was rejected | `propose_graft` duplicate guard over the complete specimen history | direct regression plus `scripts/verify_duplicate_replay.py` replay from a fresh wallet | corrected StudioNet lifecycle | PASS local source; live proof pending |
| Replays must not consume another blight mark or force `BLIGHTED` | duplicate guard runs before consensus and mutation | regression asserts unchanged blight, history length, and state | corrected StudioNet lifecycle | PASS local source; live proof pending |
| Public app must use the corrected deployment | `frontend/lib/chain.ts` | frontend build and address check | public Cloudflare build | FAIL |

Optional suggestions: none in the steward request.
