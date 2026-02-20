import { AiFillThunderbolt } from "react-icons/ai";

export default function PromoBanner() {
  return (
    <div className="flex-2 bg-[#FFFFFF] rounded-2xl p-8 flex justify-between items-center">
      {/* Left Section */}
      <div className="max-w-md">
        <p className="text-sm text-gray-400 font-medium">Built by developers</p>

        <h2 className="text-2xl font-bold text-gray-800 mt-2">
          Purity UI Dashboard
        </h2>

        <p className="text-gray-400 mt-3 text-sm leading-relaxed">
          From colors, cards, typography to complex elements, you will find the
          full documentation.
        </p>

        <button className="mt-6 text-sm font-semibold text-gray-700 flex items-center gap-2 cursor-pointer hover:gap-3 transition-all">
          Read more →
        </button>
      </div>

      {/* Right Section */}
      <div className="w-105 h-55 bg-[#4FD1C5] rounded-2xl flex items-center justify-center relative overflow-hidden">
        {/* Circles inside Chakra icon */}
        <div className="absolute w-40 h-40 bg-white/10 rounded-full -top-10 -right-10"></div>
        <div className="absolute w-32 h-32 bg-white/10 rounded-full bottom-0 left-10"></div>

        <div className="flex gap-2 items-center">
          <AiFillThunderbolt size={30} color="white" />

          <h3 className="text-white text-3xl font-semibold">chakra</h3>
        </div>
      </div>
    </div>
  );
}
