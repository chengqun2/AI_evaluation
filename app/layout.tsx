import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({ variable: "--font-geist", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Sunny Tea House · AI Review Assistant",
  description: "Turn a real tea moment into a review that sounds like you.",
  icons: { icon: "/favicon.svg", shortcut: "/favicon.svg" },
  openGraph: {
    title: "Sunny Tea House · AI Review Assistant",
    description: "喜欢这一杯？帮我们说出来。",
    type: "website",
    images: [{ url: "/og.png", width: 1792, height: 933, alt: "Sunny Tea House AI Review Assistant" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Sunny Tea House · AI Review Assistant",
    description: "喜欢这一杯？帮我们说出来。",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="zh-CN"><body className={geist.variable}>{children}</body></html>;
}
