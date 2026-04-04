import type { Metadata } from "next";
import { DM_Sans } from "next/font/google";

import "./globals.css";

const fontSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "¿Ahí es?",
  description: "Test condicional para evaluar Green Flag, Zona Gris o Red Flag.",
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
