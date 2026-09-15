# Inlane Metabase MCP server

Wraps the Metabase REST API at `https://analytics-metabase.inlane.in` as MCP tools: run SQL, browse databases/tables/fields, list and run saved questions, list and fetch dashboards.

## Setup

1. In Metabase: **Admin settings → Authentication → API Keys → Create API Key**. Copy the key.
2. Install and build:
   ```bash
   cd mcp-server/metabase
   npm install
   npm run build
   ```
3. Set environment variables (copy `.env.example` to `.env`, or export directly):
   ```
   METABASE_URL=https://analytics-metabase.inlane.in
   METABASE_API_KEY=<your key>
   ```
   Never commit `.env` or the key itself.

## Register with Claude Code

```bash
claude mcp add inlane-metabase -- node /absolute/path/to/mcp-server/metabase/dist/index.js
```

Set `METABASE_URL` and `METABASE_API_KEY` in that MCP server's environment (Claude Code prompts for env vars on `claude mcp add`, or set them in `.mcp.json`/`claude_desktop_config.json` under this server's `env` key).

## Tools

- `list_databases`
- `list_tables` (`database_id`)
- `get_table_fields` (`table_id`)
- `run_sql_query` (`database_id`, `query`, optional `row_limit`)
- `list_cards`
- `run_card` (`card_id`, optional `row_limit`)
- `list_dashboards`
- `get_dashboard` (`dashboard_id`)

`run_sql_query` and `run_card` cap returned rows at 200 by default (max 2000, via `row_limit`) — this only truncates the response, it does not add `LIMIT` to the SQL itself.
