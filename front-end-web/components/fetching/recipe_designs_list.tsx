import "server-only";

export interface RecipeDesign {
  id: number;
  name: string;
  description: string;
  thumbnail: string | null;
  predecessor: number | null;
  successor: number | null;
  url: string;
  is_active: boolean;
  is_inactive: boolean;
  is_deleted: boolean;
}

export default async function fetchRecipeDesignsList(): Promise<
  RecipeDesign[]
> {
  const recipes = await fetch(
    `${process.env.SERVER_API_URL}/management/recipe-designs/`,
    { cache: "no-store" }
  );

  if (!recipes.ok) {
    throw new Error("Failed to fetch data");
  }

  return recipes.json();
}
