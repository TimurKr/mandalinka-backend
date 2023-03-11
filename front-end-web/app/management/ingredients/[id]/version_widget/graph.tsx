import { BorderedElement } from "@/components/bordered_element";
import { IngredientVersion } from "@/components/fetching/ingredient_detail";

export default function Graph({ data }: { data: IngredientVersion }) {
  return (
    <div className="grid h-full place-content-center">
      <p>Tu raz bude graf. Alebo viac grafov na výber.</p>
    </div>
  );
}
