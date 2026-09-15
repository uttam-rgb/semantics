const METABASE_URL = process.env.METABASE_URL;
const METABASE_API_KEY = process.env.METABASE_API_KEY;

if (!METABASE_URL) {
  throw new Error("METABASE_URL environment variable is required");
}
if (!METABASE_API_KEY) {
  throw new Error("METABASE_API_KEY environment variable is required");
}

const baseUrl = METABASE_URL.replace(/\/+$/, "");

async function mbFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      "x-api-key": METABASE_API_KEY!,
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Metabase API ${res.status} ${res.statusText} on ${path}: ${body}`);
  }

  return (await res.json()) as T;
}

function unwrapList<T>(payload: T[] | { data: T[] }): T[] {
  return Array.isArray(payload) ? payload : payload.data;
}

export interface MbDatabase {
  id: number;
  name: string;
  engine: string;
  tables?: MbTable[];
}

export interface MbTable {
  id: number;
  name: string;
  display_name: string;
  schema: string | null;
  db_id: number;
}

export interface MbCard {
  id: number;
  name: string;
  description: string | null;
  collection_id: number | null;
  database_id: number;
  query_type: string;
}

export interface MbDashboard {
  id: number;
  name: string;
  description: string | null;
  collection_id: number | null;
}

export interface MbQueryResult {
  data: {
    cols: { name: string; display_name: string; base_type: string }[];
    rows: unknown[][];
  };
  row_count: number;
  status: string;
  error?: string;
}

export function listDatabases(): Promise<MbDatabase[]> {
  return mbFetch<MbDatabase[] | { data: MbDatabase[] }>("/api/database").then(unwrapList);
}

export function listTables(databaseId: number): Promise<MbTable[]> {
  return mbFetch<MbDatabase>(`/api/database/${databaseId}?include=tables`).then(
    (db) => db.tables ?? []
  );
}

export function getTableFields(tableId: number): Promise<unknown> {
  return mbFetch(`/api/table/${tableId}/query_metadata`);
}

export function runSqlQuery(databaseId: number, query: string): Promise<MbQueryResult> {
  return mbFetch<MbQueryResult>("/api/dataset", {
    method: "POST",
    body: JSON.stringify({
      type: "native",
      native: { query },
      database: databaseId,
    }),
  });
}

export function listCards(): Promise<MbCard[]> {
  return mbFetch<MbCard[] | { data: MbCard[] }>("/api/card").then(unwrapList);
}

export function runCard(cardId: number): Promise<MbQueryResult> {
  return mbFetch<MbQueryResult>(`/api/card/${cardId}/query`, { method: "POST" });
}

export function listDashboards(): Promise<MbDashboard[]> {
  return mbFetch<MbDashboard[] | { data: MbDashboard[] }>("/api/dashboard").then(unwrapList);
}

export function getDashboard(dashboardId: number): Promise<unknown> {
  return mbFetch(`/api/dashboard/${dashboardId}`);
}
