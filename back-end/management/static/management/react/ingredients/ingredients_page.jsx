import React from "react";
import { useMachine } from "@xstate/react";

import { createRouter } from "react-router-dom";

import Grid2 from "@mui/material/Unstable_Grid2";

import IngredientSelection from "./ingredient_selection.jsx";
import IngredientDetail from "./ingredient_detail.jsx";
import ErrorPage from "../error-page.jsx";

function IngredientsPage(props) {
  return (
    <Grid2 container sx={{ height: "100%" }}>
      <Grid2 xs="auto">
        <IngredientSelection ingredients={[]} />
      </Grid2>
      <Grid2 xs>
        <IngredientDetail />
      </Grid2>
    </Grid2>
  );
}

const IngredientsRouter = createBrowserRouter([
  {
    path: "/management/api/ingredients/",
    element: <IngredientsPage />,
    errorElement: <ErrorPage />,
  },
]);

export default IngredientsRouter;
