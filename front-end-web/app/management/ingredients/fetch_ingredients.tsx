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
    `${process.env.SERVER_API_URL}/management/ingredients/`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch data");
  }

  return res.json();
}
