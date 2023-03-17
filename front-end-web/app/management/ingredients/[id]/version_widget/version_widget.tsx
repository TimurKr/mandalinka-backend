import "server-only";

import fetchUnits from "@/components/fetching/units";
import { IngredientDetail } from "@/components/fetching/ingredient_detail";
import { notFound } from "next/navigation";
import dynamic from "next/dynamic";
import VersionSelector from "./version_selector";
import IngredientVersionForm from "@/components/management/ingredients/forms/ingredient_version_form";
import { BorderedElement } from "@/components/bordered_element";
import GeneralInfo from "./general";
import InStockManipulation from "./in_stock_manipulation";
import Graph from "./graph";
import StatusManipulation from "./status_manipulation";

const OrdersTable = dynamic(() => import("./orders_table"), { ssr: false });

const RemovalsTable = dynamic(() => import("./removals_table"), { ssr: false });

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
              <GeneralInfo data={current_version} />
            </BorderedElement>
          </div>
          <div className="flex-auto">
            <BorderedElement title="Graf">
              <Graph data={current_version} />
            </BorderedElement>
          </div>
          <div className="flex-auto">
            <BorderedElement title="Objednávky">
              <OrdersTable
                data={current_version}
                modify_url={`${process.env.CLIENT_API_URL}/management/ingredients/stock_orders/`}
              />
            </BorderedElement>
          </div>
          <div className="flex-auto">
            <BorderedElement title="Odpisy">
              <RemovalsTable
                data={current_version}
                delete_url={`${process.env.CLIENT_API_URL}/management/ingredients/stock_removals/`}
              />
            </BorderedElement>
          </div>
          {current_version.is_inactive && (
            <div className="flex-auto">
              <BorderedElement title="Upravte verziu" className="!pt-4">
                <IngredientVersionForm
                  submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/versions/${current_version.id}/`}
                  method="PATCH"
                  ingredient={ingredient}
                  initial={current_version}
                />
              </BorderedElement>
            </div>
          )}
          {(current_version.is_active ||
            current_version.orders.length > 0 ||
            current_version.removals.length > 0 ||
            current_version.in_stock_amount > 0) && (
            <div className="flex-initial">
              <BorderedElement title="Na sklade" className="!p-3 !pr-1">
                <InStockManipulation
                  ingredientVersion={current_version}
                  units={units}
                  CLIENT_API_URL={process.env.CLIENT_API_URL || ""}
                />
              </BorderedElement>
            </div>
          )}
          <div>
            <BorderedElement title="Zmena statusu" className="pt-3">
              <StatusManipulation
                ingredientVersion={current_version}
                CLIENT_API_URL={process.env.CLIENT_API_URL || ""}
              />
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
            submit_url={`${process.env.CLIENT_API_URL}/management/ingredients/new_version/`}
            method="POST"
            ingredient={ingredient}
          />
          <VersionSelector ingredient={ingredient} />
        </div>
      </BorderedElement>
    );
  }
}
