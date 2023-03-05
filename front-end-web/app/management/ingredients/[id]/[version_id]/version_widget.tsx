import "server-only";

import { IngredientDetail } from "@/components/fetching/ingredient_detail";
import ActionPanel from "./actions";
import { notFound } from "next/navigation";
import VersionSelector from "./version_selector";

export default function IngredientVersionWidget({
  ingredient,
  version_id,
}: {
  ingredient: IngredientDetail;
  version_id: number;
}) {
  let current = ingredient.versions.find(
    (version) => version.id === version_id
  );
  // Return not found if ingredient doesnt have version with the version_id
  if (!current) {
    return (
      <div className="truncate">
        Nieje žiadna Verzia {version_id} not in{" "}
        {JSON.stringify(ingredient.versions)}
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto">
      Niečo fajn
      <VersionSelector ingredient={ingredient} current={current?.id || "new"} />
      {/* <div>
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
      /> */}
    </div>
  );
}
