import "server-only";

import React from "react";

import fetchIngredietDetail from "@/components/fetching/ingredient_detail";

import IngredientVersionWidget from "../version_widget";
import { notFound } from "next/navigation";

export default async function Ingredient({
  params,
}: {
  params: { id: string; version_id: string };
}) {
  const ingredient = await fetchIngredietDetail(params.id);

  let current_version = ingredient.versions.find(
    (version) => version.id === parseInt(params.version_id)
  );

  if (!current_version) {
    notFound();
  }

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
