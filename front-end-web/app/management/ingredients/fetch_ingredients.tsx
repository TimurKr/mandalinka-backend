import "server-only";

export interface Ingredient {
  id: number;
  name: string;
  usage_last_month: number;
  url: string;
  is_active: boolean;
  is_inactive: boolean;
  is_deleted: boolean;
}

export default async function getData(): Promise<Ingredient[]> {
  const res = await fetch(
    "http://mandalinka.api.com:8000/management/api/ingredients/"
  );

  if (!res.ok) {
    throw new Error("Failed to fetch data");
  }

  return res.json();
}
