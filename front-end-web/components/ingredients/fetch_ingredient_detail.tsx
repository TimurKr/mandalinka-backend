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
  alergens: number[];
  status: string;
  img: string;
  cost: number;
  usage_last_month: number;
  versions: IngredientVersion[];
}

export default async function getData(id: string): Promise<IngredientDetail> {
  const res = await fetch(
    `${process.env.SERVER_API_URL}/management/ingredient/${id}/`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch data");
  }

  return res.json();
}
