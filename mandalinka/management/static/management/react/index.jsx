// This is the entry point for the Management React app.

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

import "@fontsource/noto-serif-display/300.css";
import "@fontsource/noto-serif-display/400.css";
import "@fontsource/noto-serif-display/500.css";
import "@fontsource/noto-serif-display/700.css";

import React from "react";
import $ from "jquery";
import { createRoot } from "react-dom/client";

import { CssBaseline } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";

import MandalinkaTheme from "./theme.jsx";
import ManagementPage from "./management.jsx";

$(() => {
  const root_element = $("#root");

  createRoot(root_element[0]).render(
    <ThemeProvider theme={MandalinkaTheme}>
      <CssBaseline />
      <ManagementPage
        active_path={root_element.attr("active-path")}
        url={root_element.attr("url")}
      />
    </ThemeProvider>
  );
});
