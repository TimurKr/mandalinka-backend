import "server-only";

export interface Unit {
  id: number;
  sign: string;
  name: string;
}
[];

export default async function fetchUnits(): Promise<Unit[]> {
  const units = await fetch(`${process.env.SERVER_API_URL}/management/units/`);

  if (units.ok) {
    return await units.json();
  } else {
    throw new Error("Failed to fetch units");
  }
}
