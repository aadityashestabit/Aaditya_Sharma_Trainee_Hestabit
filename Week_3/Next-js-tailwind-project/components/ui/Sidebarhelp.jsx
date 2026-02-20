import { HiQuestionMarkCircle } from "react-icons/hi2";

export default function Sidebarhelp() {
  return (
    <div className="h-42.25 w-54.5 bg-[#4FD1C5] rounded-xl flex flex-col px-3 py-2">
      <div className="px-1 mb-4 rounded-full bg-[#4FD1C5]">
        <HiQuestionMarkCircle size={40} color="white" />
      </div>

      <div className="mb-3">
        <h2 className="text-sm text-white font-bold">Need Help ?</h2>
        <p className="text-xs text-white font-medium">Please check our docs</p>
      </div>

      <button className="w-46.5 h-8.75 bg-white rounded-xl text-xs font-bold cursor-pointer">
        DOCUMENTATION
      </button>
    </div>
  );
}
