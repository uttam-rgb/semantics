# analytics."demo-payments"

**Status:** ☠️ LIKELY DEAD/SUPERSEDED — froze 2026-03-27, right around the same March 2026 cutover window as the `public`→`analytics` migration (see [`schema_map.md`](../../schema_map.md)). 108 rows, spanning 2025-07-25 to 2026-03-27.

**Note on table name:** contains a hyphen (`"demo-payments"`), unusual for this schema — must be double-quoted in SQL.

**Purpose:** Payments for trial/demo driving lessons, with marketing attribution (UTM params, `gclid`). Despite the name, **not purely test data** — amounts include both token values (₹1–2, likely test transactions) and a real-looking ₹600 demo-lesson fee, matching `payment.payment_type = 'demo'`'s existence in the current payment system.

**Working theory (unconfirmed):** this was the demo-payment flow before the same migration/cutover that froze `public`, superseded by `payment` rows with `payment_type = 'demo'` in the current system.

## Columns

`id`, `created_at`, `name`, `phone`, `email`, `amount` (bigint), `hasDrivingLicense` (boolean), `area`, `paymentStatus` (text — observed: `Not Initiated` 73, `failed` 17, `done` 16, plus one `'TEST'` and one `'h'`, both clearly junk values), `paymentMessage`, `utm_source`/`utm_medium`/`utm_campaign`/`utm_term`/`utm_content`, `gclid`.

## Gotchas

- Mixed real and test data — filter `paymentStatus NOT IN ('TEST', 'h')` at minimum, and consider the ₹1–2 amount rows as likely test transactions too.
- If demo-lesson payment history before March 2026 is ever needed, this is probably the source — but confirm the "superseded by `payment.payment_type='demo'`" theory with the owner first.

**Owner:** TBD
**Last verified:** 2026-09-12
