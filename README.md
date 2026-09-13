# Inlane Semantic Layer

A Claude Code plugin **and** documentation layer for Inlane's `cratio_crm` Postgres database — so Claude stops guessing which tables/columns map to which business metric when generating reports through Metabase.

## Table of Contents

- [Why this exists](#why-this-exists)
- [How it works](#how-it-works)
- [Install as a plugin (Claude Code)](#install-as-a-plugin-claude-code)
- [Alternative: wiring into a claude.ai Project](#alternative-wiring-into-a-claudeai-project)
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

There are two ways to actually get this into a Claude conversation, and they're not interchangeable — pick the one that matches how you're using Claude.

## Install as a plugin (Claude Code)

If you're working in **Claude Code** (this CLI/agent environment — terminal, IDE extension, or the Desktop app's Code tab), this repo installs as a real plugin. No copy-paste, no manual uploads — a Skill auto-triggers whenever you're writing SQL against this database or asking about one of its metrics, and Claude reads the relevant docs on demand.

```bash
/plugin marketplace add uttam-rgb/semantics
/plugin install inlane-semantics@inlane-semantics-marketplace
```

That's it. Ask Claude something like "what's our conversion rate this month" or "write a query against `cratio_leads_analytics`" in a Claude Code session and the skill should trigger on its own. To invoke it explicitly instead of waiting for auto-trigger:

```
/inlane-semantics:inlane-data-guide
```

**Testing a local checkout before publishing changes:**
```bash
claude --plugin-dir /path/to/this/repo
```
Then run `/help` to confirm the skill is listed, and `/reload-plugins` to pick up edits without restarting.

This only works inside Claude Code, not a claude.ai Project. For claude.ai, see the next section.

## Alternative: wiring into a claude.ai Project

For a claude.ai Project with Metabase's native MCP connector attached. Pick one option, don't combine them:

**Option A: upload as a custom Skill.** See [`CLAUDE_AI_SKILL_SETUP.md`](CLAUDE_AI_SKILL_SETUP.md). Requires a plan with code execution enabled.

**Option B: paste into Project Knowledge/custom instructions.**

1. **Custom instructions.** Open [`_index.md`](_index.md) and paste its full contents into the Project's custom instructions field.
2. **Project Knowledge.** Upload the files listed in [`PROJECT_KNOWLEDGE_UPLOAD_LIST.md`](PROJECT_KNOWLEDGE_UPLOAD_LIST.md).

## What's Inside

```
.claude-plugin/
  plugin.json                 # plugin manifest
  marketplace.json            # self-registering marketplace (this repo is its own marketplace)
skills/
  inlane-data-guide/SKILL.md  # the skill that auto-triggers in Claude Code

_index.md                    # for the claude.ai Project path (Option B): goes into custom instructions
conventions.md                # cross-cutting rules: stale-number handling, naming, known-bad fields
schema_map.md                 # which schema/table is authoritative when public/analytics duplicate each other
open_questions.md             # ~50 items discovered during documentation that still need a human answer
future_work.md                # what's left to document, and why it was deprioritized
PROJECT_KNOWLEDGE_UPLOAD_LIST.md  # exactly what to upload where for the claude.ai Project path (Option B)
inlane-data-guide.zip          # claude.ai custom-Skill upload (Option A) — see CLAUDE_AI_SKILL_SETUP.md
CLAUDE_AI_SKILL_SETUP.md       # how to install/update the Skill zip above

tables/
  exotel/                     # 2 tables
  public/                     # 21 tables
  analytics/                  # 84 tables
metrics/                       # 16 business-metric docs

SQL_Logic/                     # production Metabase SQL, used as ground truth for the metrics above
reference/                     # Lane_Metric_Definitions_v1.xlsx — the Analytics team's own metric spec
scripts/                       # Python/psycopg2 scripts used to introspect the schema (read-only);
                                # build_claude_ai_skill.py regenerates inlane-data-guide.zip
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
5. Commit and push. **Plugin users get the update automatically** next time Claude Code checks the marketplace (or via `/plugin marketplace update`); **claude.ai Project users don't** — re-upload the changed files to the Project's Knowledge base by hand, there's no auto-sync there.
6. If the change affects a hard rule, update `skills/inlane-data-guide/SKILL.md` and `_index.md` together — they carry the same rules for the two different consumption paths and should stay in sync.

## Philosophy

- **Ground truth over guesswork** — a metric's definition comes from production code or the business, never from staring at a table and taking a guess.
- **Flag ambiguity, don't resolve it silently** — an unconfirmed mapping stays unconfirmed in the docs until someone with the authority to confirm it does.
- **Numbers are snapshots, not facts** — every row count in these docs was true once, on its "Last verified" date. Query the live table for a current answer; use the doc for the durable finding underneath the number.
- **Verify, then write it down** — nothing gets asserted from a table or column name alone if the live data can confirm or contradict it directly.

## Security

`config.yaml` (database credentials) and any raw schema/data dump under `scripts/` are gitignored. Never commit credentials to this repo.
