import "server-only";

import React from "react";

import IngredientForm from "@/components/management/ingredients/forms/ingredient_form";

import fetchAlergens from "@/components/fetching/alergens";
import fetchUnits from "@/components/fetching/units";
import fetchIngredietDetail from "@/components/fetching/ingredient_detail";
import { BorderedElement } from "@/components/bordered_element";
import Button from "@/components/button";
import { ArrowLeftIcon } from "@heroicons/react/20/solid";

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
    <BorderedElement className="!p-0">
      <div className="relative h-full">
        <Button
          href={`/management/ingredients/${params.id}/`}
          className="absolute top-0 left-2 flex !w-auto items-center bg-inherit"
          color="black"
        >
          <ArrowLeftIcon className="mr-1 h-4 w-4" />
          Verzie
        </Button>
        <IngredientForm
          title="Upravte ingredienciu"
          submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/${params.id}/`}
          method="PATCH"
          options={{ alergens: alergens, units: units }}
          initial={ingredient}
        />
      </div>
    </BorderedElement>
  );
}
