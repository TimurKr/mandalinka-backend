import fetchAttributes from "@/components/fetching/attributes";
import fetchDiets from "@/components/fetching/diets";
import fetchUnits from "@/components/fetching/units";
import fetchKitchenAccesories from "@/components/fetching/kitchen_accesories";
import RecipeDesignForm from "@/components/management/recipes/forms/recipe_design_form";
import fetchRecipeDesignsList from "@/components/fetching/recipe_designs_list";
import fetchIngredients from "@/components/fetching/ingredients_list";

export default async function Ingredients() {
  const units_promise = fetchUnits();
  const attributes_promise = fetchAttributes();
  const diets_promise = fetchDiets();
  const kitchen_accesories_promise = fetchKitchenAccesories();
  const recipe_designs_promise = await fetchRecipeDesignsList();
  const ingredients_promise = await fetchIngredients();

  const [units, attributes, diets, kitchen_accesories, recipes, ingrediencie] =
    await Promise.all([
      units_promise,
      attributes_promise,
      diets_promise,
      kitchen_accesories_promise,
      recipe_designs_promise,
      ingredients_promise,
    ]);

  const options = {
    units: units.map((u) => ({ value: u.id.toString(), label: u.name })),
    attributes: attributes.map((a) => ({
      value: a.id.toString(),
      label: a.name,
    })),
    diets: diets.map((d) => ({ value: d.id.toString(), label: d.name })),
    kitchen_accesories: kitchen_accesories.map((k) => ({
      value: k.id.toString(),
      label: k.name,
    })),
    recipes: recipes.map((r) => ({ value: r.id.toString(), label: r.name })),
    ingredients: ingrediencie.map((i) => ({
      value: i.id.toString(),
      label: i.name,
    })),
  };

  return (
    <div className="grid h-full place-content-center">
      <RecipeDesignForm
        title="Vyrobte nový recept"
        submit_url="#"
        method="POST"
        options={options}
      />
    </div>
  );
}
