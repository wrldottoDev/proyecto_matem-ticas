import type { Metadata } from "next";
import { DM_Sans } from "next/font/google";

import "./globals.css";

const fontSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "¿Ahí es?",
  description: "Descubrí si tu situación relacional es una Green Flag, una Zona Gris o una Red Flag.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={`${fontSans.variable} bg-aurora font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
