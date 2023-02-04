import { createTheme, responsiveFontSizes } from "@mui/material/styles";

const MandalinkaTheme = responsiveFontSizes(
  createTheme({
    palette: {
      mode: "dark",
      primary: {
        main: "#F28500",
      },
      secondary: {
        main: "#ff9800",
      },
    },
    typography: {
      fontFamily:
        '"Noto Serif Display", "Roboto", "Helvetica", "Arial", sans-serif',
    },
    spacing: (factor) => `${0.5 * factor}rem`,
  })
);

export default MandalinkaTheme;
