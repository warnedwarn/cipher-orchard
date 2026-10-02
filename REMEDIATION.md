# Steward remediation

| Mandatory requirement | Code path | Targeted proof | Deployment proof | Status |
| --- | --- | --- | --- | --- |
| Reject a duplicate graft even when its first attempt was rejected | `propose_graft` duplicate guard over the complete specimen history | `tests/direct/test_duplicate_graft.py` replays a rejected graft from a fresh wallet | corrected source deployed at `0x06864b30c52Fd1873269E3EE9DF8a62222697555` | PASS source and targeted regression |
| Replays must not consume another blight mark or force `BLIGHTED` | duplicate guard runs before consensus and mutation | regression asserts unchanged blight, history length, and state | deployment transaction finalized with successful execution | PASS source and targeted regression |
| Public app must use the corrected deployment | `frontend/lib/chain.ts` | typecheck, static build, production bundle address check, and browser inspection | `https://cipher-orchard.pages.dev/` | PASS |

Optional suggestions: none in the steward request.

The current StudioNet endpoint returns an undefined-method runtime error for calls against both the prior and corrected deployments. This network incident prevents a new live replay trace; it does not alter the complete-history guard or its direct regression. The repository records the limitation instead of presenting finality as successful execution.
