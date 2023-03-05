import "server-only";

import fetchUnits from "@/components/fetching/units";
import { IngredientDetail } from "@/components/fetching/ingredient_detail";
import ActionPanel from "./[version_id]/actions";
import { notFound } from "next/navigation";
import VersionSelector from "./[version_id]/version_selector";
import IngredientVersionForm from "@/components/management/ingredients/forms/ingredient_version_form";

export default async function IngredientVersionWidget({
  ingredient,
  version_id,
}: {
  ingredient: IngredientDetail;
  version_id?: number;
}) {
  const unit_options = await fetchUnits();

  let current = ingredient.versions.find(
    (version) => version.id === version_id
  );
  // Return not found if ingredient doesnt have version with the version_id
  if (!current && version_id) {
    return notFound();
  }

  if (version_id) {
    return (
      <div className="relative flex h-full justify-between overflow-visible p-2 pt-3">
        <VersionSelector ingredient={ingredient} current_id={version_id} />
        <div>Info</div>
        <div>Info</div>
        <div>Info</div>
        <div>Info</div>
        {/* <ActionPanel api_host={process.env.CLIENT_API_URL} ingredient={ingredient} version_id={version_id}/> */}
      </div>
    );
  } else {
    return (
      <div className="relative h-full w-full overflow-visible p-2 pt-3">
        <IngredientVersionForm
          title="Nová verzia ingrediencie"
          submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/${ingredient.id}/new_version/`}
          method="POST"
          unit_options={unit_options}
          ingredient={ingredient}
        />
        <VersionSelector ingredient={ingredient} />
      </div>
    );
  }
}
