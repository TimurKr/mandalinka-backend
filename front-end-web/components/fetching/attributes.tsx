import "server-only";

export interface Attribute {
  id: number;
  name: string;
  icon: string;
}

export default async function fetchAttributes(): Promise<Attribute[]> {
  const attributes = await fetch(
    `${process.env.SERVER_API_URL}/management/attributes/`
  );

  if (attributes.ok) {
    return await attributes.json();
  } else {
    throw new Error("Failed to fetch attributes");
  }
}
