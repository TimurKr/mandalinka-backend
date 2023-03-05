import "server-only";

import fetchIngredientDetail from "@/components/fetching/ingredient_detail";
import ActionPanel from "./actions";
import { notFound } from "next/navigation";

export default async function IngredientVersion({
  params,
}: {
  params: { id: string; version_id: string };
}) {
  const ingredient = await fetchIngredientDetail(params.id);
  const ingredient_version = ingredient.versions.find(
    (version) => version.id.toString() === params.version_id
  );
  // Return not found if ingredient doesnt have version with the version_id
  if (!ingredient_version) {
    notFound();
  }

  return (
    <div className="max-h-full overflow-auto">
      <div>
        Tu bude detail o verzií ingrediencie. Možno nejaký fancy graf, ešte
        uvidíme čo bude treba.
      </div>
      <div>
        <h2>Available data</h2>
        <pre className="text-ellipsis text-xs">
          {JSON.stringify(ingredient_version, null, 2)}
        </pre>
      </div>
      <ActionPanel
        api_host={process.env.CLIENT_API_URL}
        ingredient={ingredient}
        version_id={params.version_id}
      />
    </div>
  );
}
