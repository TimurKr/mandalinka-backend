import React from "react";

export default function IngredientsPage({ active_path, url }) {
  return (
    <div>
      <div>Ingredients</div>
      <div>Ďalšia cesta: {active_path}</div>
      <div>Url to load on render: {url}</div>
    </div>
  );
}
