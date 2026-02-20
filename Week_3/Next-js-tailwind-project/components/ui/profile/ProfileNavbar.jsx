"use client";

import { FiSearch } from "react-icons/fi";
import { MdPerson } from "react-icons/md";
import { IoSettingsOutline } from "react-icons/io5";
import { IoNotificationsOutline } from "react-icons/io5";

export default function ProfileNavbar({ pageName }) {
  return (
    <nav className="w-full bg-transparent px-8 py-4 flex  justify-between items-center">
      {/* Left Section */}
      <div>
        <div className="text-sm  text-gray-100">
          Pages <span className=" mx-1 text-gray-100">/</span>
          <span className="text-gray-100">{pageName}</span>
        </div>

        <h2 className="text-sm font-semibold text-gray-100 mt-1">{pageName}</h2>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-6">
        <div className="flex items-center bg-white border h-[39.5px] w-56 border-gray-200 rounded-xl px-4 py-2 w-56">
          <FiSearch className="text-gray-100 font-extrabold mr-2" size={14} />
          <input
            type="text"
            placeholder="Type here..."
            className="w-full text-sm outline-none bg-transparent text-gray-700 placeholder-gray-400"
          />
        </div>

        <div className="flex items-center gap-1 text-gray-100 font-bold text-sm cursor-pointer">
          <MdPerson size={16} />
          <span>Sign In</span>
        </div>

        <IoSettingsOutline
          size={18}
          className="text-gray-100 font-extrabold cursor-pointer"
        />

        <IoNotificationsOutline
          size={18}
          className="text-gray-100 font-extrabold cursor-pointer"
        />
      </div>
    </nav>
  );
}
