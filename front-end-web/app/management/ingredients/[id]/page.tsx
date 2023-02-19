import React from "react";

import getData from "./fetch_ingredient_detail";

export default async function Ingredient({
  params,
}: {
  params: { id: string };
}) {
  const ingredient = await getData(params.id);

  return (
    <div>
      Tu bude detail o ingrediencií. Možno nejaký fancy graf, ešte uvidíme čo
      bude treba.
    </div>
  );
}
