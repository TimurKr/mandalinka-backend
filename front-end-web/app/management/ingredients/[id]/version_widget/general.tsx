import { IngredientVersion } from "@/components/fetching/ingredient_detail";
import { Unit } from "@/components/fetching/units";

export default function GeneralInfo({
  data,
  units,
}: {
  data: IngredientVersion;
  units: Unit[];
}) {
  return (
    <>
      <div className="grid h-full w-full place-content-center">
        <p>Dodávatel: {data.source}</p>
        <p>
          Cena: {data.cost} € /{" "}
          {units.find((unit) => unit.id === data.unit)?.sign}
        </p>
      </div>
    </>
  );
}
