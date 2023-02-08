import { createTheme, responsiveFontSizes } from "@mui/material/styles";
import { grey } from "@mui/material/colors";

const MandalinkaTheme = responsiveFontSizes(
  createTheme({
    palette: {
      // mode: "dark",
      primary: {
        main: "#FFAF87",
      },
      secondary: {
        main: "#C0B580",
      },
    },
    typography: {
      fontFamily:
        '"Noto Serif Display", "Roboto", "Helvetica", "Arial", sans-serif',
      caption: {
        display: "block",
        color: grey[700],
      },
    },

    components: {
      MuiButtonBase: {
        defaultProps: {
          disableRipple: true,
        },
        styleOverrides: {
          root: {
            borderRadius: "10px",
            transition: "'all' 1s",
            "&:hover": {
              boxShadow: "0 0 20px rgba(0,0,0,0.19)",
            },
          },
        },
      },
      MuiIconButton: {
        defaultProps: {
          color: "black",
        },
        styleOverrides: {
          root: {
            borderRadius: "0.5rem",
            transition: "'all' 1s",
            color: "black",
            "&:hover": {
              backgroundColor: "inherit",
              boxShadow: "0 0 20px rgba(0,0,0,0.19)",
            },
          },
        },
        variants: [
          {
            props: { variant: "selected" },
            style: {
              color: "#FFAF87",
            },
          },
        ],
      },
      MuiOutlinedInput: {
        styleOverrides: {
          root: {
            borderRadius: "1rem",
          },
        },
      },
    },
  })
);

export default MandalinkaTheme;
