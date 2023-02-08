import React from "react";

import { AppBar, Toolbar, Icon, Typography } from "@mui/material";
import { FoodBank } from "@mui/icons-material";

export default function Header({ open }) {
  return (
    <AppBar position="fixed">
      <Toolbar>
        <Icon color="black" aria-label="mandalinka logo" edge="start">
          <FoodBank />
        </Icon>
        <Typography variant="h4" noWrap component="div">
          Mandalinka Management Page
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
