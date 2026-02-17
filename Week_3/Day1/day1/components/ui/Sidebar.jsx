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

export default function Sidebar() {
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
        <h1 className="text-sm font-bold leading-none">PURITY AI DASHBOARD</h1>
      </div>

      <div className="space-y-4 mb-16">
        {/* Home  */}
        <SidebarItem
          label="Dashboard"
          href="#"
          active={true}
          icon={<MdHome size={15} color="#4FD1C5" />}
        />

        {/* Tables */}

        <SidebarItem
          label="Tables"
          href="#"
          icon={<IoStatsChartSharp size={15} color="#4FD1C5" />}
        />

        {/* Billing */}

        <SidebarItem
          label="Billing"
          href="#"
          icon={<FaCreditCard size={15} color="#4FD1C5" />}
        />

        {/* RTL */}

        <SidebarItem
          label="RTL"
          href="#"
          icon={<FiTool size={15} color="#4FD1C5" />}
        />

        <h2 className="text-sm font-bold">Account Pages</h2>

        {/* Profile */}

        <SidebarItem
          label="Profile"
          href="#"
          icon={<CgProfile size={15} color="#4FD1C5" />}
        />

        {/* SignIn */}

        <SidebarItem
          label="Sign In"
          href="#"
          icon={<FaFile size={15} color="#4FD1C5" />}
        />

        {/* SignUp */}

        <SidebarItem
          label="Sign Up"
          href="#"
          icon={<IoIosRocket size={15} color="#4FD1C5" />}
        />
      </div>

      <Sidebarhelp />
    </aside>
  );
}
