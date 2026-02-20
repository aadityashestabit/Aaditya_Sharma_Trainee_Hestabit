import Link from "next/link";

export default function SidebarItem({ label, href, active, icon }) {
  return (
    <Link
      href={href}
      className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-all duration-200
        ${
          active
            ? "bg-white text-gray-600 font-bold"
            : "text-gray-600 hover:bg-gray-200 hover:text-gray-700"
        }`}
    >
      <div className="rounded-full bg-[#FFFFFF] p-2 h-7.5 w-7.5 text-center">
        {icon}
      </div>
      <span className="text-xs">{label}</span>
    </Link>
  );
}
