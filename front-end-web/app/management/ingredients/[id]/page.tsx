import "server-only";

import React from "react";

import ActionPanel from "./actions";

import fetchIngredietDetail from "@/components/fetching/ingredient_detail";

import IngredientVersionWidget from "./version_widget";

export default async function Ingredient({
  params,
}: {
  params: { id: string };
}) {
  const ingredient = await fetchIngredietDetail(params.id);

  let current_version =
    ingredient.versions.find((version) => version.is_active) ||
    ingredient.versions.find((version) => version.is_inactive) ||
    ingredient.versions.find((version) => version.is_deleted) ||
    ingredient.versions[-1] ||
    undefined;

  return (
    <>
      {/* @ts-expect-error Async Server Component */}
      <IngredientVersionWidget
        ingredient={ingredient}
        version_id={current_version?.id}
      />
    </>
  );
}
