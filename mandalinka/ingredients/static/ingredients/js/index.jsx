import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import React from "react";
import IngredientManagementPage from "./includes/management_page.jsx";

const root_element = document.getElementById("ingredient-management-page");
const search_url = root_element.getAttribute("search-url");
const ingredient_url = root_element.getAttribute("ingredient-url");

const root = createRoot(document.getElementById("ingredient-management-page"));

root.render(
  // <StrictMode>
  <IngredientManagementPage
    search_url={search_url}
    ingredient_url={ingredient_url}
  />
  // </StrictMode>
);
