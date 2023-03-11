import "server-only";

import React from "react";

import fetchIngredietDetail from "@/components/fetching/ingredient_detail";

import IngredientVersionWidget from "../version_widget/version_widget";

export default async function Ingredient({
  params,
}: {
  params: { id: string; version_id: string };
}) {
  const ingredient = await fetchIngredietDetail(params.id);

  return (
    <>
      {/* @ts-expect-error Async Server Component */}
      <IngredientVersionWidget ingredient={ingredient} />
    </>
  );
}
