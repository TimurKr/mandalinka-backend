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

export default async function fetchIngredientsList(): Promise<Ingredient[]> {
  const ingredient = await fetch(
    `${process.env.SERVER_API_URL}/management/ingredients/`,
    { next: { revalidate: 5 } }
  );

  if (!ingredient.ok) {
    throw new Error("Failed to fetch data");
  }

  return ingredient.json();
}
