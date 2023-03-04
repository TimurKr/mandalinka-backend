import "server-only";

export interface Options {
  alergens: { code: number; name: string }[];
  units: { id: number; sign: string; name: string }[];
}

export default async function getOptions(): Promise<Options> {
  const alergensPromise = fetch(
    `${process.env.SERVER_API_URL}/management/alergens/`
  );
  const unitsPromise = fetch(`${process.env.SERVER_API_URL}/management/units/`);

  const [alergens, units] = await Promise.all([alergensPromise, unitsPromise]);

  return {
    alergens: await alergens.json(),
    units: await units.json(),
  };
}
