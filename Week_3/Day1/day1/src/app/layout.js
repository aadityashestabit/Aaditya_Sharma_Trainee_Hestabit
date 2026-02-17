import { Poppins } from "next/font/google";
import "./globals.css";
import Sidebar from "../../components/ui/Sidebar";
import Navbar from "../../components/ui/Navbar";
// import Footer from "../../components/ui/Footer";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
});


export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`flex bg-gray-100 ${poppins.className}`} >
        <Sidebar />
        <div className="flex flex-col flex-1">
          <Navbar/>
          <main >
          {children}
        </main>
        {/* <Footer/> */}
        </div>
        
      </body>
    </html>
  );
}
