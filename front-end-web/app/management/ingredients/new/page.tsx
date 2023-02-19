import React from "react";

import NewIngredientForm from "./form";

export default function NewIngredient() {
  function handleSubmit(event: React.ChangeEvent<HTMLFormElement>): void {
    event.preventDefault();
    console.log("Submitted");
  }
  return (
    <div>
      <NewIngredientForm />
    </div>
  );
}
