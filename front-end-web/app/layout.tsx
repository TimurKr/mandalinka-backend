import "./globals.css";

import { Noto_Serif_Display } from "next/font/google";

import "material-symbols/outlined.css";
import "material-symbols/rounded.css";

const font = Noto_Serif_Display({
  subsets: ["latin-ext"],
  display: "swap",
});

export const metadata = {
  title: {
    default: "Mandalinka",
    template: "%s | Mandalinka",
  },
  description: "Mandalinka webpage",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="sk" className={font.className}>
      {/*
        <head /> will contain the components returned by the nearest parent
        head.tsx. Find out more at https://beta.nextjs.org/docs/api-reference/file-conventions/head
      */}
      {/* <head /> */}
      <body>{children}</body>
    </html>
  );
}
