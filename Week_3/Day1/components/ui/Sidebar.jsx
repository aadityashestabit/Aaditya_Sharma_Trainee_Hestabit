"use client";
import Image from "next/image";
import SidebarItem from "./SidebarItem";
import { MdHome } from "react-icons/md";
import { IoStatsChartSharp } from "react-icons/io5";
import { FaCreditCard } from "react-icons/fa";
import { CgProfile } from "react-icons/cg";
import { FaFile } from "react-icons/fa";
import { IoIosRocket } from "react-icons/io";
import { FiTool } from "react-icons/fi";
import Sidebarhelp from "./Sidebarhelp";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-61.5 min-h-screen bg-gray-100  p-6">
      <div className="flex items-center gap-3 mb-8">
        <Image
          src="/images/purity_logo.png"
          alt="Purity Logo"
          width={22}
          height={22}
          className="object-contain"
        />
        <h1 className="text-sm font-bold leading-none">PURITY UI DASHBOARD</h1>
      </div>

      <div className="space-y-4 mb-16">
        <SidebarItem
          label="Dashboard"
          href="/dashboard"
          active={pathname === "/dashboard"}
          icon={<MdHome size={15} color="#4FD1C5" />}
        />

        <SidebarItem
          label="Tables"
          href="/tables"
          active={pathname === "/tables"}
          icon={<IoStatsChartSharp size={15} color="#4FD1C5" />}
        />

        <SidebarItem
          label="Billing"
          href="#"
          active={pathname === "/billing"}
          icon={<FaCreditCard size={15} color="#4FD1C5" />}
        />

        <SidebarItem
          label="RTL"
          href="#"
          active={pathname === "/rtl"}
          icon={<FiTool size={15} color="#4FD1C5" />}
        />

        <h2 className="text-sm font-bold">Account Pages</h2>

        <SidebarItem
          label="Profile"
          href="/profile"
          active={pathname === "/profile"}
          icon={<CgProfile size={15} color="#4FD1C5" />}
        />

        <SidebarItem
          label="Sign In"
          href="/sign-in"
          active={pathname === "/sign-in"}
          icon={<FaFile size={15} color="#4FD1C5" />}
        />

        <SidebarItem
          label="Sign Up"
          href="/sign-up"
          active={pathname === "/sign-up"}
          icon={<IoIosRocket size={15} color="#4FD1C5" />}
        />
      </div>

      <Sidebarhelp />
    </aside>
  );
}
