import "server-only";

import React from "react";

import IngredientForm from "components/ingredients/forms/ingredient_form";

import getOptions from "components/ingredients/forms/fetch_options";

export default async function NewIngredient() {
  const options = await getOptions();

  return (
    <div className="grid h-full place-content-center">
      <IngredientForm
        title="Pridajte novú ingredienciu"
        submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/`}
        method="POST"
        options={options}
      />
    </div>
  );
}
