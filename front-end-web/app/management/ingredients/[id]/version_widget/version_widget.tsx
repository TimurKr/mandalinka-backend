import "server-only";

import fetchUnits from "@/components/fetching/units";
import { IngredientDetail } from "@/components/fetching/ingredient_detail";
import { notFound } from "next/navigation";
import VersionSelector from "./version_selector";
import IngredientVersionForm from "@/components/management/ingredients/forms/ingredient_version_form";
import { BorderedElement } from "@/components/bordered_element";
import GeneralInfo from "./general";
import OrdersTable from "./orders_table";
import InStockManipulation from "./in_stock_manipulation";
import Graph from "./graph";
import StatusManipulation from "./status_manipulation";

export default async function IngredientVersionWidget({
  ingredient,
  version_id,
}: {
  ingredient: IngredientDetail;
  version_id?: number;
}) {
  const units = await fetchUnits();

  let current_version = ingredient.versions.find(
    (version) => version.id === version_id
  );
  // Return not found if ingredient doesnt have version with the version_id
  if (!current_version && version_id) {
    return notFound();
  }

  if (current_version) {
    return (
      <BorderedElement
        className={`relative !p-0 ${
          current_version.is_active
            ? "!border-green-600"
            : current_version.is_inactive
            ? "!border-yellow-600"
            : current_version.is_deleted
            ? "!border-red-600"
            : "!border-gray-600"
        }`}
      >
        <div>
          <VersionSelector ingredient={ingredient} current_id={version_id} />
        </div>
        <div className="flex h-full flex-wrap justify-between gap-3 overflow-visible p-2 pt-4">
          <div className="shrink-0">
            <BorderedElement title="Všeobecné informácie">
              <GeneralInfo data={current_version} units={units} />
            </BorderedElement>
          </div>
          <div className="flex-auto">
            <BorderedElement>
              <Graph data={current_version} />
            </BorderedElement>
          </div>
          <div className="flex-auto">
            <BorderedElement className="!p-0 " title="Objednávky">
              <OrdersTable data={current_version} />
            </BorderedElement>
          </div>
          <div className="flex-auto">
            <BorderedElement>
              <IngredientVersionForm
                submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/versions/${current_version.id}/`}
                method="PATCH"
                unit_options={units}
                ingredient={ingredient}
              />
            </BorderedElement>
          </div>
          <div className="shrink-0">
            <BorderedElement title="Na sklade" className="!p-3">
              <InStockManipulation data={current_version} units={units} />
            </BorderedElement>
          </div>
          <div className="shrink-0">
            <BorderedElement title="Zmena statusu">
              <StatusManipulation />
            </BorderedElement>
          </div>
        </div>
      </BorderedElement>
    );
  } else {
    return (
      <BorderedElement className="!border-primary-600 !p-0">
        <div className="relative h-full w-full overflow-visible p-2 pt-4">
          <IngredientVersionForm
            title="Nová verzia ingrediencie"
            submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/${ingredient.id}/new_version/`}
            method="POST"
            unit_options={units}
            ingredient={ingredient}
          />
          <VersionSelector ingredient={ingredient} />
        </div>
      </BorderedElement>
    );
  }
}
