# "Lane Cars" — a separate used-car marketplace side business

`car_inventory`, `sell_leads`, and `buyer_request` don't belong to the driving-school business at all — they're a **used-car buying/selling marketplace**, most likely the "Lane Cars" feature referenced in `analytics.earning_program` (a referral program paying instructors ₹1,500 per car sale referral, `key = 'lane_cars'`). **This connection is a strong inference from the data, not explicitly confirmed by the business owner** — confirm before treating it as fact in a business-facing report.

## The three tables

- **`car_inventory`** (147 rows) — used cars currently listed for sale: seller contact, make/model/year, price, EMI, condition, photos.
- **`sell_leads`** (408 rows) — leads from people wanting to **sell** their car (registration, make/model, condition, ownership history). Likely feeds `car_inventory` once a car is accepted/listed.
- **`buyer_request`** (38 rows) — leads from people wanting to **buy** a car (budget, body type, fuel, transmission preference). The demand side, to be matched against `car_inventory`.

No enforced FKs between any of these three, or to any of the driving-school tables (`Learner`, `Instructor`, etc.) — if a relationship exists (e.g., which instructor referred a given `sell_leads`/`buyer_request` row), it isn't captured at the database level here.

## Supporting evidence found since

`analytics.Learner` (not `public.Learner`) has a whole set of car-purchase-intent columns (`car_purchase_timeline`, `car_intent_planning`, `car_intent_type`, `car_intent_condition`, `car_intent_timeframe`, `car_intent_source`, etc.) — car-buying interest is captured directly on the learner profile. This strengthens the Lane Cars connection further, but there's still no FK from `Learner` to `car_inventory`/`sell_leads`/`buyer_request`.

## Open questions

- Confirm with the owner: is this genuinely the "Lane Cars" business referenced in `earning_program`?
- Is this business unit in scope for the same semantic layer/reporting effort as the driving school, or should it be documented separately for a different audience?
- No visible link from a `sell_leads`/`buyer_request` row back to the referring instructor — if the ₹1,500 referral payout needs to be tracked, where does that attribution happen?
