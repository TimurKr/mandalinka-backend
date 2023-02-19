import "server-only";

export interface IngredientVersion {
  version_number: number;
  url: string;
  is_active: boolean;
  is_inactive: boolean;
  is_deleted: boolean;
}

export interface IngredientDetail {
  id: number;
  name: string;
  unit: string;
  cost: number;
  usage_last_month: number;
  versions: IngredientVersion[];
}

export default async function getData(id: string): Promise<IngredientDetail> {
  const res = await fetch(
    `http://mandalinka.api.com:8000/management/api/ingredient/${id}/`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch data");
  }

  return res.json();
}
