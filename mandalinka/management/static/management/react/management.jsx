import React from "react";
import { useState } from "react";

import PageDrawer from "./page_drawer.jsx";
import IngredientsPage from "./ingredients/ingredient_page.jsx";

import Box from "@mui/material/Box";

import EggAltOutlinedIcon from "@mui/icons-material/EggAltOutlined";
import FastfoodOutlinedIcon from "@mui/icons-material/FastfoodOutlined";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";
import DeliveryDiningOutlinedIcon from "@mui/icons-material/DeliveryDiningOutlined";

export default function ManagementPage({ active_path, url }) {
  const PAGES = {
    null: {
      element: <div>Zvolte si stránku</div>,
      icon: undefined,
      title: null,
    },
    deliveries: {
      element: <div>Deliveries</div>,
      icon: <DeliveryDiningOutlinedIcon />,
      title: "Doručenia",
    },
    menus: {
      element: <div>Menus</div>,
      icon: <CalendarMonthOutlinedIcon />,
      title: "Menu",
    },
    recipes: {
      element: <div>Recipes</div>,
      icon: <FastfoodOutlinedIcon />,
      title: "Recepty",
    },
    ingredients: {
      element: (
        <IngredientsPage
          active_path={active_path.split("/").slice(1).join("/") || null}
          url="Heel"
        />
      ),
      icon: <EggAltOutlinedIcon />,
      title: "Suroviny",
    },
  };

  function get_page(path) {
    const path_components = path.split("/");
    if (path_components.length == 0 || path.length == 0) {
      console.log("No active path");
      return "null";
    } else if (!(path_components[0] in PAGES)) {
      console.log("Invalid active path");
      return "null";
    } else {
      console.log("Valid active path");
      return path_components[0];
    }
  }

  const [page, setPage] = useState(get_page(active_path));

  function handlePageChange(new_page) {
    if (new_page == page) {
      setPage("null");
    } else {
      setPage(new_page);
    }
  }

  return (
    <Box sx={{ display: "flex" }}>
      <PageDrawer
        active_page={page}
        handlePageChange={handlePageChange}
        pages={Object.entries(PAGES).map(([key, value]) => ({
          id: key,
          title: value.title,
          icon: value.icon,
          active: page === key,
        }))}
      />
      {PAGES[page].element}
    </Box>
  );
}
