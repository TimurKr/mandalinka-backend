import "server-only";

import React from "react";

import IngredientForm from "@/components/management/ingredients/forms/ingredient_form";

import fetchAlergens from "@/components/fetching/alergens";
import fetchUnits from "@/components/fetching/units";

export default async function NewIngredient() {
  const alergensPromise = fetchAlergens();
  const unitsPromise = fetchUnits();

  const [alergens, units] = await Promise.all([alergensPromise, unitsPromise]);

  return (
    <div className="grid h-full place-content-center">
      <IngredientForm />
    </div>
  );
}
