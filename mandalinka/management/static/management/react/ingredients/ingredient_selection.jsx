import React from "react";

import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Card from "@mui/material/Card";
import Box from "@mui/material/Box";

import VerticalPanel from "../custom_elements/VerticalPanel.jsx";

export default function IngredientSelection({ ingredients }) {
  function handleIngredientSelection(ingredient) {
    console.log(ingredient);
  }

  return (
    <VerticalPanel sx={{ padding: 1 }}>
      <TextField label="Hľadať ingredienciu" variant="outlined" />
      {ingredients.map((ingredient) => (
        <Typography variant="body1" sx={{ padding: 1 }}>
          {ingredient.name}
        </Typography>
      ))}
    </VerticalPanel>
  );
}
