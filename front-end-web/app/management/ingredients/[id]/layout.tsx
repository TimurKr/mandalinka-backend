import VersionSelector from "./version_widget/version_selector";
import Image from "next/image";

import fetchIngredietDetail from "@/components/fetching/ingredient_detail";
import fetchAlergens from "@/components/fetching/alergens";
import fetchUnits from "@/components/fetching/units";
import Button from "@/components/button";
import { BorderedElement } from "@/components/bordered_element";

export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { id: string };
}) {
  const ingredientPromise = fetchIngredietDetail(params.id);
  const alergensPromise = fetchAlergens();
  const unitsPromise = fetchUnits();

  const [ingredient, alergens, units] = await Promise.all([
    ingredientPromise,
    alergensPromise,
    unitsPromise,
  ]);

  return (
    <div className="flex w-full max-w-6xl flex-row flex-wrap self-start justify-self-center">
      <div className="w-full flex-shrink-0 p-2">
        <h3
          className={`text-4xl ${
            ingredient.is_active
              ? "text-green-500"
              : ingredient.is_deleted
              ? "text-red-500"
              : ingredient.is_inactive
              ? "text-yellow-500"
              : "text-gray-500"
          }`}
        >
          {ingredient.name}
        </h3>
      </div>
      <div className="aspect-square shrink-0 basis-full p-2 md:basis-1/3">
        <BorderedElement className="relative">
          {ingredient.img ? (
            <Image
              className="inset-0 aspect-square h-auto w-auto rounded-xl object-cover"
              src={ingredient.img}
              alt={ingredient.name}
              width={512}
              height={512}
            />
          ) : (
            <Image
              className="rounded-xl"
              src="/ingredient_placeholder.png"
              alt={ingredient.name}
              fill={true}
            />
          )}
        </BorderedElement>
      </div>
      <div className="shrink-0 flex-grow basis-full p-2 md:basis-2/3">
        <BorderedElement>
          <h4 className="text-xl">Graf používanie v minulosti</h4>
          <p>TODO: Graf používanie v minulosti</p>
        </BorderedElement>
      </div>
      <div className="flex-1 basis-1/4 p-2">
        <BorderedElement>
          Extra info: {ingredient.extra_info || "N/A"}
        </BorderedElement>
      </div>
      <div className="flex-1 shrink-0 basis-1/4 p-2">
        <BorderedElement>
          <h4>Alergény:</h4>
          <p className="text-sm text-gray-400">
            {alergens
              .filter((alergen) => ingredient.alergens.includes(alergen.code))
              .map((alergen) => alergen.code + ": " + alergen.name)
              .join("\n") || "žiadne"}
          </p>
        </BorderedElement>
      </div>
      <div className="flex-1 basis-1/4 p-2">
        <BorderedElement>
          Cena: {ingredient.cost ? ingredient.cost.toString() + " €" : "N/A"}
        </BorderedElement>
      </div>
      <div className="flex-1 basis-1/4 p-2">
        <BorderedElement>
          Na sklade: {ingredient.in_stock_amount} {ingredient.unit.sign}
        </BorderedElement>
      </div>
      <div className="flex-1 basis-1/4 p-2">
        <Button
          color="black"
          href={`/management/ingredients/${ingredient.id}/edit/`}
        >
          Edit
        </Button>
      </div>

      <div className="mt-4 min-h-[256px] basis-full p-2">{children}</div>
    </div>
  );
}
