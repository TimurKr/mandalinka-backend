import "server-only";

export interface Diet {
  id: number;
  name: string;
  icon: string;
}

export default async function fetchDiets(): Promise<Diet[]> {
  const alergens = await fetch(
    `${process.env.SERVER_API_URL}/management/diets/`
  );

  if (alergens.ok) {
    return await alergens.json();
  } else {
    throw new Error("Failed to fetch diets");
  }
}
