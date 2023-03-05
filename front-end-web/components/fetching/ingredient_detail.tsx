import "server-only";

import { notFound } from "next/navigation";

export interface IngredientVersion {
  id: number;
  ingredient: number;
  version_number: number;
  cost: number;
  url: string;
  is_active: boolean;
  is_inactive: boolean;
  is_deleted: boolean;
  unit: number;
  source: string;
}

export interface IngredientDetail {
  id: number;
  name: string;
  unit: number;
  alergens: number[];
  status: string;
  is_active: boolean;
  is_inactive: boolean;
  is_deleted: boolean;
  in_stock_amount: boolean;
  img: string;
  cost: number;
  usage_last_month: number;
  versions: IngredientVersion[];
}

export default async function fetchIngredientDetail(
  id: string
): Promise<IngredientDetail> {
  const ingredient = await fetch(
    `${process.env.SERVER_API_URL}/management/ingredients/${id}/`,
    { next: { revalidate: 5 } }
  );

  if (!ingredient.ok) {
    if (ingredient.status === 404) {
      notFound();
    }
    throw new Error(`Failed to fetch data for ingredient with id: ${id}.`);
  }

  return await ingredient.json();
}
