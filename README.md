# Inlane Semantic Layer

A documentation layer for Inlane's `cratio_crm` Postgres database, built so Claude (and anyone else) stops guessing which tables/columns map to which business metric when generating reports through Metabase.

## Why this exists

Inlane's revenue team went self-serve on reporting — connecting Claude to Metabase to build reports and metrics on demand. The numbers came out wrong. Not because Claude can't write SQL, but because it had no grounding on which of several similarly-named tables was authoritative, which `lead_stage` values counted as "converted," which date field a metric should filter on, or that a column like `call_did_status` looks trustworthy but isn't. This repo is that grounding.

## What's here

```
_index.md                    # goes into a Claude Project's custom instructions (hard rules + index)
conventions.md                # cross-cutting rules: stale-number handling, naming, known-bad fields
schema_map.md                 # which schema/table is authoritative when public/analytics duplicate each other
open_questions.md             # ~49 items discovered during documentation that still need a human answer
future_work.md                # what's left to document, and why it was deprioritized
PROJECT_KNOWLEDGE_UPLOAD_LIST.md  # exactly what to upload where when wiring this into a Claude Project

tables/
  exotel/                     # 2 tables
  public/                     # 21 tables
  analytics/                  # 84 tables
metrics/                       # 16 business-metric docs

SQL_Logic/                     # production Metabase SQL, used as ground truth for the metrics above
reference/                     # Lane_Metric_Definitions_v1.xlsx — the Analytics team's own metric spec
scripts/                       # Python/psycopg2 scripts used to introspect the schema (read-only)
```

**Every table doc** follows the same shape: Status (live/stale/dead/superseded), Purpose, Grain, Columns, Relationships, Gotchas, Owner, Last verified.

**Every metric doc** has a YAML front-matter block (`status: confirmed|draft|deprecated`, `source`, `dimensions`, `confirmed_by`) followed by a `verified_sql` section — a tested query to use as a template, not just a description of the logic.

## Ground truth, not guesswork

Nothing here is asserted from schema shape alone. Every table finding and every metric formula was checked against the live database (row counts, freshness, ID overlaps, actual value distributions) and, where possible, against two independent real sources:

1. **Production Metabase SQL** (`SQL_Logic/*.sql`) — the queries actually driving Inlane's dashboards today.
2. **`Lane_Metric_Definitions_v1.xlsx`** (`reference/`) — the Analytics team's own semantic spec for the same dashboards.

Where those two disagreed with each other, or with what the schema itself implied, the conflict is documented and adjudicated explicitly rather than silently resolved — see `open_questions.md` and the "Adjudicated" notes inside individual metric docs. A few real production bugs were found this way (e.g. an "overdue followups" alert that didn't actually filter for overdue-ness) and are flagged, not quietly fixed.

## Key findings if you're new here

- **`public` and `analytics` are not a "core vs. reporting" split.** For most shared tables, `public` is a fork frozen around March 2026; `analytics` has everything `public` has plus everything since. Two tables (`Admin`, `admin_permissions`) don't follow this pattern at all — see `schema_map.md`.
- **`analytics.cratio_leads_analytics.call_did_status` must never be used for anything.** It doesn't populate reliably — checked against real telephony data (`public.exotel_calls`) and found almost entirely disjoint.
- **"Agent" means `lead_owner`.** Every "X by agent" metric is an existing metric grouped by that column, not a separate concept.
- Two whole subsystems live in the `analytics` schema whose relevance to this semantic layer is **unconfirmed**: a used-car marketplace ("Lane Cars") and a geospatial demand/supply planning system (H3 hex-grid based) that may belong to a separate project entirely. See `future_work.md` before treating either as in scope.

## Using this with Claude

1. Paste `_index.md`'s contents into the Claude Project's **custom instructions** field.
2. Upload the files listed in `PROJECT_KNOWLEDGE_UPLOAD_LIST.md` as **Project Knowledge**. Do not upload `config.yaml`, anything under `scripts/`, or the raw `SQL_Logic/*.sql` files (some contain known bugs — the corrected, annotated versions live in `metrics/*.md`).
3. Metabase's native MCP server (or whichever query tool the Project uses) stays the execution layer — this repo is what tells Claude *which* query to build before it calls those tools, not a replacement for them.

## Extending this

New table or new metric, same process throughout this repo:

1. Introspect against the live database with a read-only credential (see `scripts/` for the pattern — pull columns, constraints, comments, row counts, and freshness; only fall back to a higher-privilege credential for schemas the read-only role lacks grants on).
2. Write the doc following the existing template (table or metric, whichever applies).
3. If it resolves or raises an open question, update `open_questions.md`. If it changes which table/schema is authoritative, update `schema_map.md`.
4. Never assert a metric's business definition from data exploration alone — get it from production SQL, a spreadsheet/spec the business already maintains, or the data owner directly. Exploration is for *verifying* a definition, not *inventing* one.
5. Commit, then re-upload the changed files to the Claude Project's Knowledge base (there's no auto-sync).

## What not to commit

`config.yaml` (database credentials) and any raw schema/data dump under `scripts/` are gitignored. Never commit credentials to this repo, even in a private one.
