import React from "react";
import Box from "@mui/material/Box";
import { styled } from "@mui/material/styles";

const VerticalPanel = styled(Box)(({ theme }) => ({
  height: "100%",
  padding: 1,
  boxShadow: `5px 0 10px 0 rgba(0, 0, 0, 0.06)`,
}));

export default VerticalPanel;
