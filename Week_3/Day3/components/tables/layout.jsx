import { Poppins } from "next/font/google";
import Sidebar from "../../../components/ui/Sidebar";
import Navbar from "../../../components/ui/Navbar";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
});

export default function DashBoardLayout({ children }) {
  return (
    <div className={`flex bg-gray-100 min-h-screen ${poppins.className}`}>
      <Sidebar />

      <div className="flex flex-col flex-1">
        <Navbar pageName="Tables" />
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
