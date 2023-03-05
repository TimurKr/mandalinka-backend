import "server-only";

import React from "react";

import IngredientForm from "@/components/management/ingredients/forms/ingredient_form";

import fetchAlergens from "@/components/fetching/alergens";
import fetchUnits from "@/components/fetching/units";
import fetchIngredietDetail from "@/components/fetching/ingredient_detail";

export default async function NewIngredient({
  params,
}: {
  params: { id: string };
}) {
  const alergensPromise = fetchAlergens();
  const unitsPromise = fetchUnits();
  const ingredientPromise = await fetchIngredietDetail(params.id);

  const [alergens, units, ingredient] = await Promise.all([
    alergensPromise,
    unitsPromise,
    ingredientPromise,
  ]);

  return (
    <div>
      <IngredientForm
        title="Upravte ingredienciu"
        submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/${params.id}/`}
        method="PATCH"
        options={{ alergens: alergens, units: units }}
        initial={ingredient}
      />
    </div>
  );
}
