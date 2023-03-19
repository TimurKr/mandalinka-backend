import "server-only";

export interface KitchenAccessory {
  id: number;
  name: string;
  icon: string;
}

export default async function fetchKitchenAccessories(): Promise<
  KitchenAccessory[]
> {
  const response = await fetch(
    `${process.env.SERVER_API_URL}/management/kitchen-accesories/`,
    { cache: "no-store" }
  );

  if (response.ok) {
    return await response.json();
  } else {
    throw new Error("Failed to fetch kitchen acessories");
  }
}
