import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "VoxCraft",
  description: "Offline STT/TTS platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
