export default function StatCard({icon,label,amount,percentage}) {
  return (
    <div className="bg-[#FFFFFF] rounded-2xl px-6 py-5 flex justify-between items-center flex-1 h-20 shadow-sm">
      
      {/* Left Content */}
      <div>
        <p className="text-sm text-gray-400 font-bold">
          {label}
        </p>

        <div className="flex items-center gap-2 mt-1">
          <h2 className="text-lg font-bold text-gray-800">
            ${amount}
          </h2>

          <span className="text-green-500 font-bold text-sm">
            {percentage}%
          </span>
        </div>
      </div>

      {/* Right Teal Box */}
      <div className="w-12 h-12 flex justify-center items-center bg-[#4FD1C5] rounded-xl">{icon}</div>
      
    </div>
  );
}
