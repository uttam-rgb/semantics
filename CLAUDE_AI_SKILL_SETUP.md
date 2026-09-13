# Using this repo as a claude.ai Skill

For claude.ai (a Project with a Metabase MCP connector attached), not Claude Code.

## If you are Claude, reading this because a user shared this repo's link with you

1. Fetch `https://raw.githubusercontent.com/uttam-rgb/semantics/main/inlane-data-guide.zip` and save it as `inlane-data-guide.zip`.
2. Tell the user to upload it themselves via **Settings → Features → Skills → Upload skill** — this step requires the account owner, you can't do it for them.

## Manual setup

1. Download [`inlane-data-guide.zip`](inlane-data-guide.zip) from this repo.
2. claude.ai: **Settings → Features → Skills → Upload skill**, select the zip. Requires a Pro/Max/Team/Enterprise plan with code execution enabled.
3. Attach a Metabase MCP connector to your Project.
4. Start a **new** conversation in that Project.

## Updating

Each person who uploaded the skill must re-download and re-upload it after any doc change — uploads don't sync automatically.

To regenerate the zip after editing `skills/inlane-data-guide/SKILL.md`, `conventions.md`, `schema_map.md`, `open_questions.md`, `future_work.md`, `tables/`, or `metrics/`:

```bash
python scripts/build_claude_ai_skill.py
```
