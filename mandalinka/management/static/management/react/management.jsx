import React from "react";
import { useState } from "react";

import IngredientsRouter from "./ingredients/ingredients_page.jsx";

import VerticalPanel from "./custom_elements/VerticalPanel.jsx";

import Grid2 from "@mui/material/Unstable_Grid2";
import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import IconButton from "@mui/material/IconButton";

import EggAltOutlinedIcon from "@mui/icons-material/EggAltOutlined";
import FastfoodOutlinedIcon from "@mui/icons-material/FastfoodOutlined";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";
import DeliveryDiningOutlinedIcon from "@mui/icons-material/DeliveryDiningOutlined";
import { RouterProvider } from "react-router-dom";

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
      element: <RouterProvider router={IngredientsRouter} />,
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
    <Grid2 container sx={{ height: "100vh" }}>
      <Grid2 xs="auto">
        <VerticalPanel
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            padding: 1,
          }}
        >
          {Object.entries(PAGES).map(([key, data]) => {
            if (data.icon === undefined) return null;
            return (
              <Tooltip key={key} title={data.title} placement="right" arrow>
                {/* Icon to change the page. If active, use "selected" variant */}
                <IconButton
                  sx={{ marginY: 0.5 }}
                  onClick={() => handlePageChange(key)}
                  variant={key == page ? "selected" : null}
                >
                  {data.icon}
                </IconButton>
              </Tooltip>
            );
          })}
        </VerticalPanel>
      </Grid2>
      <Grid2 xs>{PAGES[page].element}</Grid2>
    </Grid2>
  );
}
