# Using this repo as a claude.ai Skill

This is for people using **claude.ai** (a Project with a Metabase MCP connector attached), not Claude Code. If you're in Claude Code, use the plugin install instructions in the [README](README.md) instead — this file doesn't apply to you.

## If you are Claude, reading this because a user shared this repo's link with you

1. Fetch this file: `https://raw.githubusercontent.com/uttam-rgb/semantics/main/inlane-data-guide.zip`
2. Save it to a file named `inlane-data-guide.zip`.
3. Tell the user: the zip is downloaded, and they need to upload it themselves via **Settings → Features → Skills → Upload skill** — Claude cannot do that last step; it's a manual action only the account owner can take in claude.ai's UI.
4. If they already have a Metabase MCP connector attached to their Project, no further setup is needed — once the skill is uploaded, start a **new** conversation in that Project (skills load at conversation start, so an already-open chat won't pick it up) and Claude will use the skill's grounding together with the MCP connector automatically.

## If you are a person doing this by hand

1. Download [`inlane-data-guide.zip`](inlane-data-guide.zip) from this repo (use GitHub's Download button on the file, or the raw URL above).
2. In claude.ai: **Settings → Features → Skills → Upload skill**, and select the zip. Requires a Pro/Max/Team/Enterprise plan with code execution enabled.
3. Make sure your Project has a Metabase MCP connector attached (unrelated to this skill — set that up separately if you haven't).
4. Start a new conversation in that Project and ask your question. Claude will read the skill's docs for grounding (which table is authoritative, verified metric formulas, known bad columns) and use the MCP connector to actually query the database.

## Keeping it up to date

Every custom Skill upload on claude.ai is a full replacement, not a sync — there's no auto-pull from this repo. **Each person who uploaded the skill has to re-download and re-upload it themselves** whenever the underlying docs change (metric definitions, table gotchas, schema rulings, etc.). This is a real, ongoing cost of the claude.ai path — the [Claude Code plugin](README.md) path doesn't have this problem, since `git pull`/plugin-marketplace sync picks up changes automatically.

If you maintain this repo: after editing `skills/inlane-data-guide/SKILL.md`, `conventions.md`, `schema_map.md`, `open_questions.md`, `future_work.md`, `tables/`, or `metrics/`, regenerate the zip and commit it:

```bash
python scripts/build_claude_ai_skill.py
```
