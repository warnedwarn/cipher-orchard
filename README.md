# CIPHER ORCHARD

Specimen entry: a cooperative semantic puzzle that grows only when independent validators agree that a player's graft fits the frozen clues and rule.

StudioNet contract: `0x359959431F3EB99Ee45378Bce2ADf531df4c7251`

Live specimen: `https://cipher-orchard.pages.dev/`  
Source notebook: `https://github.com/warnedwarn/cipher-orchard`

## Growth law

A curator plants one specimen with public clues, a private-style written rule, a bloom goal, and a finite blight limit. Every wallet may submit one novel graft. Accepted grafts raise bloom by exactly one. Rejected grafts consume one blight mark. The first terminal boundary produces `BLOOMED` or `BLIGHTED`.

GenLayer is load-bearing because semantic fit cannot be reduced to a deterministic string comparison and no single game host should control shared progress.

## Graft protocol

`plant_specimen` freezes clues and bounds. `propose_graft` rejects duplicate wallets, duplicate accepted grafts, short reasoning, and closed specimens before calling AI. Validators assess the same rule, clues, accepted history, candidate, and reasoning. Code then normalizes contradictory results, mutates only one counter, and derives terminal state.

Paged reads are `get_specimens_page` and `get_grafts_page`. Focused reads are `get_specimen` and `get_summary`.

## Validator notes

A candidate is not accepted merely because it returns valid JSON. The validator independently checks whether the proposed result applies the frozen rule without contradiction or rule drift. The contract stores only the bounded fit decision, conflicts, and compact note.

## Cultivation commands

```text
cd frontend
npm install
npm run typecheck
npm run build
```

```text
genvm-lint check contracts/contract.py
python -m pytest tests/test_surface.py -q
node scripts/no-emoji.js
node scripts/no-emdash.js
```

## Field cautions

The hidden-rule rubric is visible in contract state to validators and should be treated as a consensus puzzle rule, not a cryptographic secret. The installed Windows direct runner currently fails during SDK loading, so full validator behavior must be verified on StudioNet. The frontend is a static Next.js puzzle surface with read-only hydration, browser-wallet writes, and no traditional backend.
