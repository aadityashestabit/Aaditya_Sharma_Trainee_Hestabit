import "./globals.css";
import Sidebar from "../../components/ui/Sidebar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="flex bg-gray-100">
        <Sidebar />
        <main className="flex-1 p-1">
          {children}
        </main>
      </body>
    </html>
  );
}
