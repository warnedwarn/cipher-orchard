# Cultivation verification

## Local observations

- GenVM AST lint: passed.
- Contract surface suite: 4 passed.
- TypeScript: passed.
- Static build: passed.
- Emoji and em dash scans: passed.

## Network observations

Corrected contract `0x06864b30c52Fd1873269E3EE9DF8a62222697555` deployed in transaction `0x74b9568041d348313ff000d810afc4a42c023073bb8c2d5cabc344aa08e4243d` with `MAJORITY_AGREE` and leader execution `SUCCESS`. It contains source SHA-256 `f1b0d6766290268fe42d3a335bc9e24c2ba39c887ec8a2554bff3b9bf2b54aad` from commit `2e3f1684dd6ad2e807c4f9201b80b68bb54c7ddf`.

The live replay script is included, but current calls to both the prior and corrected deployments return the same StudioNet undefined-method runtime error. The attempted plant transaction `0x4f3ea4623e76f09349eecc3b37a6d93f53ac3c0d485cfddfd46eeef94461d7e8` finalized with `ERROR`, so it is not represented as successful proof. The direct regression remains the executable proof artifact; on this Windows host the upstream direct runner fails during SDK import with `unexpected end of memory`, before the contract test body executes.

GitHub publication succeeded. Cloudflare production returned HTTP 200 with title `Cipher Orchard`, the corrected address in the production bundle, the expected application shell, and no browser console errors.
