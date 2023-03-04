import VersionSelector from "./version_selector";

import getData from "../../../../components/ingredients/fetch_ingredient_detail";

export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { id: string };
}) {
  const ingredient = await getData(params.id);

  return (
    <div className="flex h-full w-full flex-col">
      <div className="flex-shrink">
        Detail ingrediencie {ingredient.name}
        <div className="float-right">
          <VersionSelector
            ingredient_id={ingredient.id.toString()}
            versions={ingredient.versions.reverse()}
          />
        </div>
      </div>
      <div className="grid flex-auto place-content-center">{children}</div>
    </div>
  );
}
