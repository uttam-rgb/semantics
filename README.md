# Inlane Semantic Layer

A documentation layer for Inlane's `cratio_crm` Postgres database, built so Claude (and anyone else) stops guessing which tables/columns map to which business metric when generating reports through Metabase.

## Table of Contents

- [Why this exists](#why-this-exists)
- [How it works](#how-it-works)
- [Getting Started](#getting-started)
- [What's Inside](#whats-inside)
- [Key Findings](#key-findings-if-youre-new-here)
- [Extending This](#extending-this)
- [Philosophy](#philosophy)
- [Security](#security)

## Why this exists

Inlane is moving towards self-serve reporting — letting the team connect Claude to Metabase and build their own reports and metrics on demand, instead of routing every request through a data/analytics person. That only works if Claude has real grounding: which of several similarly-named tables is authoritative, which `lead_stage` values actually count as "converted," which date field a metric should filter on, and that a column like `call_did_status` looks trustworthy but isn't. An early attempt without that grounding produced wrong numbers — not because Claude can't write SQL, but because nothing told it which SQL was right. This repo is that grounding.

## How it works

Every table and every metric in this database gets one short, self-contained doc — never inferred from a name or a hunch. A table doc says what it actually holds, what one row means, and what will trip you up. A metric doc says the exact formula and carries a query that's already been run against real data, not just described.

Nothing here is asserted from schema shape alone. Every finding was checked against the live database (row counts, freshness, ID overlaps, actual value distributions) and, where possible, against two independent real sources of truth: Inlane's actual production Metabase SQL, and the Analytics team's own metric-definitions spreadsheet. Where those two disagreed with each other — or with what the schema itself implied — the conflict is written down and resolved explicitly, not smoothed over. A few real production bugs were caught this way and are flagged, not quietly patched.

Not everything gets an answer. Roughly 50 open questions are logged as genuinely unresolved — ambiguous status vocabularies, schema pairs nobody's confirmed the authority of, metrics that can't be built with the data that exists today. The rule throughout: **if it isn't confirmed, say so — don't guess.**

## Getting Started

This repo isn't a plugin — there's no install command that wires it up automatically. Whoever's using it with Claude needs to do two manual steps once, in their own Claude Project:

1. **Custom instructions.** Open [`_index.md`](_index.md) and paste its full contents into the Project's custom instructions field. This is the part that's always loaded, every conversation — the hard rules (which schema to trust, which fields never to use, what "agent" means) live here so they're never missed.
2. **Project Knowledge.** Upload the files listed in [`PROJECT_KNOWLEDGE_UPLOAD_LIST.md`](PROJECT_KNOWLEDGE_UPLOAD_LIST.md) — every file under `tables/` and `metrics/`, plus `conventions.md`, `schema_map.md`, and `open_questions.md`. That same file also lists what **not** to upload (`config.yaml`, anything in `scripts/`, and the raw `SQL_Logic/*.sql` files — some contain known bugs; the corrected versions live in `metrics/*.md`).

That's it — no build step, no server, no dependencies. The Metabase MCP connector (or whichever query tool the Project uses) stays the execution layer; this repo just tells Claude *which* query to build before it calls those tools.

**If you're sharing this repo with someone else**, point them at this section first. The link alone doesn't do anything — someone still has to do these two steps in their own Project.

## What's Inside

```
_index.md                    # goes into a Claude Project's custom instructions (hard rules + index)
conventions.md                # cross-cutting rules: stale-number handling, naming, known-bad fields
schema_map.md                 # which schema/table is authoritative when public/analytics duplicate each other
open_questions.md             # ~50 items discovered during documentation that still need a human answer
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

## Key Findings if you're new here

- **`public` and `analytics` are not a "core vs. reporting" split.** For most shared tables, `public` is a fork frozen around March 2026; `analytics` has everything `public` has plus everything since. Two tables (`Admin`, `admin_permissions`) don't follow this pattern at all — see `schema_map.md`.
- **`analytics.cratio_leads_analytics.call_did_status` must never be used for anything.** It doesn't populate reliably — checked against real telephony data (`public.exotel_calls`) and found almost entirely disjoint.
- **"Agent" means `lead_owner`.** Every "X by agent" metric is an existing metric grouped by that column, not a separate concept.
- Two whole subsystems live in the `analytics` schema whose relevance to this semantic layer is **unconfirmed**: a used-car marketplace ("Lane Cars") and a geospatial demand/supply planning system (H3 hex-grid based) that may belong to a separate project entirely. See `future_work.md` before treating either as in scope.

## Extending This

New table or new metric, same process throughout this repo:

1. Introspect against the live database with a read-only credential (see `scripts/` for the pattern — pull columns, constraints, comments, row counts, and freshness; only fall back to a higher-privilege credential for schemas the read-only role lacks grants on).
2. Write the doc following the existing template (table or metric, whichever applies).
3. If it resolves or raises an open question, update `open_questions.md`. If it changes which table/schema is authoritative, update `schema_map.md`.
4. Never assert a metric's business definition from data exploration alone — get it from production SQL, a spreadsheet/spec the business already maintains, or the data owner directly. Exploration is for *verifying* a definition, not *inventing* one.
5. Commit, then re-upload the changed files to the Claude Project's Knowledge base — there's no auto-sync between this repo and the Project.

## Philosophy

- **Ground truth over guesswork** — a metric's definition comes from production code or the business, never from staring at a table and taking a guess.
- **Flag ambiguity, don't resolve it silently** — an unconfirmed mapping stays unconfirmed in the docs until someone with the authority to confirm it does.
- **Numbers are snapshots, not facts** — every row count in these docs was true once, on its "Last verified" date. Query the live table for a current answer; use the doc for the durable finding underneath the number.
- **Verify, then write it down** — nothing gets asserted from a table or column name alone if the live data can confirm or contradict it directly.

## Security

`config.yaml` (database credentials) and any raw schema/data dump under `scripts/` are gitignored. Never commit credentials to this repo.
