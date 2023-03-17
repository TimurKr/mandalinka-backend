import { BorderedElement } from "@/components/bordered_element";
import { IngredientVersion } from "@/components/fetching/ingredient_detail";
import { Unit } from "@/components/fetching/units";

export default function GeneralInfo({ data }: { data: IngredientVersion }) {
  return (
    <>
      <div className="grid h-full w-full place-content-center">
        <p>{data.source}</p>
        <p>
          {data.cost ? (
            <>
              {data.cost} € / {data.unit.sign}
            </>
          ) : (
            <span className="text-xs text-gray-400">Cena nedefinovaná</span>
          )}
        </p>
      </div>
    </>
  );
}
