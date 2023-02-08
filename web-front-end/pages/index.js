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
import { StrictMode } from "react";

import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider } from "@mui/material/styles";

// import MandalinkaTheme from "./theme.jsx";
// import ManagementPage from "./management.jsx";
// import ErrorPage from "./error-page.jsx";

export default function ManagementPage() {
  return (
    <StrictMode>
      {/* <ThemeProvider theme={MandalinkaTheme}> */}
      <CssBaseline />
      {/* <ManagementPage active_path={root_element.attr("active-path")} /> */}
      <p>Hello, world!</p>
      {/* </ThemeProvider> */}
    </StrictMode>
  );
}
