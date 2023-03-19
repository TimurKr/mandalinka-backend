import "server-only";

import { notFound } from "next/navigation";
import { Unit } from "@/components/fetching/units";

export interface Order {
  id: number;
  ingredient_version: number;
  amount: number;
  unit: Unit;
  description: string;
  order_date: string;
  delivery_date: string;
  is_delivered: boolean;
  expiration_date: string;
  is_expired: boolean;
  cost: number;
  in_stock_amount: number;
}

export interface Removal {
  id: number;
  ingredient_version: number;
  amount: number;
  unit: Unit;
  reason: string;
  description: string;
  date: string;
}

export interface StockChange {
  id: number;
  ingredient_version: number;
  amount: number;
  unit: Unit;
}

export interface IngredientVersion {
  id: number;
  ingredient: number;
  version_number: number;
  cost: number | null;
  url: string;
  is_active: boolean;
  is_inactive: boolean;
  is_deleted: boolean;
  unit: Unit;
  source: string;
  expiration_period: number;
  in_stock_amount: number;
  stock_changes: StockChange[];
  orders: Order[];
  removals: Removal[];
}

export interface IngredientDetail {
  id: number;
  name: string;
  extra_info: string;
  unit: Unit;
  alergens: number[];
  status: string;
  is_active: boolean;
  is_inactive: boolean;
  is_deleted: boolean;
  img: string | null;
  cost: number | null;
  usage_last_month: number;
  in_stock_amount: number;
  versions: IngredientVersion[];
}

export default async function fetchIngredientDetail(
  id: string
): Promise<IngredientDetail> {
  const ingredient = await fetch(
    `${process.env.SERVER_API_URL}/management/ingredients/${id}/`,
    { cache: "no-store" }
  );

  if (!ingredient.ok) {
    if (ingredient.status === 404) {
      notFound();
    }
    throw new Error(`Failed to fetch data for ingredient with id: ${id}.`);
  }

  return await ingredient.json();
}
