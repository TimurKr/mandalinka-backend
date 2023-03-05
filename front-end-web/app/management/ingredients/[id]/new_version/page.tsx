import "server-only";

import IngredientVersionForm from "@/components/management/ingredients/forms/ingredient_version_form";

import fetchIngredientDetail from "@/components/fetching/ingredient_detail";
import fetchUnits from "@/components/fetching/units";

export default async function NewVersion({
  params,
}: {
  params: { id: string };
}) {
  const unitsPromise = await fetchUnits();
  const ingredientPromise = await fetchIngredientDetail(params.id);

  const [units, ingredient] = await Promise.all([
    unitsPromise,
    ingredientPromise,
  ]);

  return (
    <div>
      <IngredientVersionForm
        title={`Nová verzia ingrediencie: ${ingredient.name}`}
        submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/${params.id}/new_version/`}
        method="POST"
        unit_options={units}
        ingredient={ingredient}
      />
    </div>
  );
}
