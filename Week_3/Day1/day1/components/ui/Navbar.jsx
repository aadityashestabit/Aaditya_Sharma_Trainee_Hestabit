"use client";

import { FiSearch } from "react-icons/fi";
import { MdPerson } from "react-icons/md";
import { IoSettingsOutline } from "react-icons/io5";
import { IoNotificationsOutline } from "react-icons/io5";

export default function Navbar() {
  return (
    <nav className="w-full bg-gray-100 px-8 py-4 flex justify-between items-center">
      {/* Left Section */}
      <div>
        <div className="text-xs text-gray-400">
          Pages <span className="text-gray-300 mx-1">/</span>
          <span className="text-gray-600">Dashboard</span>
        </div>

        <h2 className="text-sm font-semibold text-gray-800 mt-1">Dashboard</h2>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-6">
        <div className="flex items-center bg-white border h-[39.5px] w-56 border-gray-200 rounded-xl px-4 py-2 w-56">
          <FiSearch className="text-gray-800 font-extrabold mr-2" size={14} />
          <input
            type="text"
            placeholder="Type here..."
            className="w-full text-sm outline-none bg-transparent text-gray-700 placeholder-gray-400"
          />
        </div>

        <div className="flex items-center gap-1 text-gray-500 font-bold text-sm cursor-pointer">
          <MdPerson size={16} />
          <span>Sign In</span>
        </div>

        <IoSettingsOutline
          size={18}
          className="text-gray-500 font-extrabold cursor-pointer"
        />

        <IoNotificationsOutline
          size={18}
          className="text-gray-500 font-extrabold cursor-pointer"
        />
      </div>
    </nav>
  );
}
