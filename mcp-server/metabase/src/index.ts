#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as mb from "./metabaseClient.js";

const DEFAULT_ROW_LIMIT = 200;

function textResult(value: unknown) {
  return { content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }] };
}

function truncateRows(result: mb.MbQueryResult, rowLimit: number) {
  const rows = result.data.rows;
  const truncated = rows.length > rowLimit;
  return {
    status: result.status,
    error: result.error,
    columns: result.data.cols.map((c) => c.display_name || c.name),
    row_count_returned: Math.min(rows.length, rowLimit),
    row_count_total: result.row_count,
    truncated,
    rows: rows.slice(0, rowLimit),
  };
}

const server = new McpServer({ name: "inlane-metabase-mcp", version: "1.0.0" });

server.tool(
  "list_databases",
  "List every database connected to this Metabase instance, with id, name, and engine.",
  {},
  async () => textResult(await mb.listDatabases())
);

server.tool(
  "list_tables",
  "List the tables in a given Metabase database (by database id from list_databases).",
  { database_id: z.number().int().describe("Metabase database id") },
  async ({ database_id }) => textResult(await mb.listTables(database_id))
);

server.tool(
  "get_table_fields",
  "Get field/column metadata (names, types) for a given table (by table id from list_tables).",
  { table_id: z.number().int().describe("Metabase table id") },
  async ({ table_id }) => textResult(await mb.getTableFields(table_id))
);

server.tool(
  "run_sql_query",
  "Run a native SQL query against a Metabase database and return the results. Use list_databases to find the database_id first.",
  {
    database_id: z.number().int().describe("Metabase database id to run the query against"),
    query: z.string().describe("Raw SQL to execute"),
    row_limit: z
      .number()
      .int()
      .positive()
      .max(2000)
      .optional()
      .describe(`Max rows to return (default ${DEFAULT_ROW_LIMIT}, max 2000). Does not change the SQL itself, only truncates the response.`),
  },
  async ({ database_id, query, row_limit }) => {
    const result = await mb.runSqlQuery(database_id, query);
    return textResult(truncateRows(result, row_limit ?? DEFAULT_ROW_LIMIT));
  }
);

server.tool(
  "list_cards",
  "List saved questions (cards) in Metabase, with id, name, and which collection/database they belong to.",
  {},
  async () => textResult(await mb.listCards())
);

server.tool(
  "run_card",
  "Run an existing saved question (card) by id and return its results.",
  {
    card_id: z.number().int().describe("Metabase card (saved question) id"),
    row_limit: z
      .number()
      .int()
      .positive()
      .max(2000)
      .optional()
      .describe(`Max rows to return (default ${DEFAULT_ROW_LIMIT}, max 2000).`),
  },
  async ({ card_id, row_limit }) => {
    const result = await mb.runCard(card_id);
    return textResult(truncateRows(result, row_limit ?? DEFAULT_ROW_LIMIT));
  }
);

server.tool(
  "list_dashboards",
  "List dashboards in Metabase, with id, name, and description.",
  {},
  async () => textResult(await mb.listDashboards())
);

server.tool(
  "get_dashboard",
  "Get a dashboard's detail, including the cards placed on it, by dashboard id.",
  { dashboard_id: z.number().int().describe("Metabase dashboard id") },
  async ({ dashboard_id }) => textResult(await mb.getDashboard(dashboard_id))
);

const transport = new StdioServerTransport();
await server.connect(transport);
