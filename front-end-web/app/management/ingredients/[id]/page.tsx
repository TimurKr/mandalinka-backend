import "server-only";

import React from "react";

import ActionPanel from "./actions";

import getData from "../../../../components/ingredients/fetch_ingredient_detail";

export default async function Ingredient({
  params,
}: {
  params: { id: string };
}) {
  const ingredient = await getData(params.id);

  const delete_url = `${process.env.CLIENT_API_URL}/management/ingredient/${params.id}`;

  return (
    <div>
      <div>
        Tu bude detail o ingrediencií. Možno nejaký fancy graf, ešte uvidíme čo
        bude treba.
      </div>
      <ActionPanel
        edit_url={`/management/ingredients/${params.id}/edit`}
        delete_url={delete_url}
      />
    </div>
  );
}
