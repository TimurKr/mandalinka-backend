import "server-only";

import React from "react";

import IngredientForm from "components/ingredients/forms/ingredient_form";

import getOptions from "components/ingredients/forms/fetch_options";
import getData from "components/ingredients/fetch_ingredient_detail";

export default async function NewIngredient({
  params,
}: {
  params: { id: string };
}) {
  const options = await getOptions();
  const ingredient = await getData(params.id);

  return (
    <div>
      <IngredientForm
        title="Upravte ingredienciu"
        submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/`}
        method="PUT"
        options={options}
        initial={ingredient}
      />
    </div>
  );
}
