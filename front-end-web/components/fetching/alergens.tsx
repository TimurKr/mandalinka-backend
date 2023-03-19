import "server-only";

export interface Alergen {
  code: number;
  name: string;
}

export default async function fetchAlergens(): Promise<Alergen[]> {
  const alergens = await fetch(
    `${process.env.SERVER_API_URL}/management/alergens/`
  );

  if (alergens.ok) {
    return await alergens.json();
  } else {
    throw new Error("Failed to fetch alergens");
  }
}
