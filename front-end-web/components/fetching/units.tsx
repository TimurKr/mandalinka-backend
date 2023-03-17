import "server-only";

export interface BaseUnit {
  id: number;
  sign: string;
  name: string;
}

export interface Unit {
  id: number;
  base_unit: BaseUnit | null;
  name: string;
  sign: string;
  conversion_rate: string;
  system: string;
  property: string;
}

export default async function fetchUnits(): Promise<Unit[]> {
  const units = await fetch(`${process.env.SERVER_API_URL}/management/units/`);

  if (units.ok) {
    return await units.json();
  } else {
    throw new Error("Failed to fetch units");
  }
}
