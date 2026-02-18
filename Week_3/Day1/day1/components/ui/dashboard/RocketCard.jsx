import Image from "next/image";

export default function RocketCard() {
  return (
    <div className="relative flex-1 h-72.5 rounded-2xl overflow-hidden shadow-md">
      
      {/* Background Image */}
      <Image
        src="/images/Background (1).png" 
        alt="Work with Rockets"
        fill
        className="object-cover scale-y-120 scale-x-120"
        priority
      />

      
      <div className="absolute inset-0 bg-black/40"></div>

      {/* Content */}
      <div className="absolute inset-0 flex flex-col justify-between p-6">
        
        {/* Text Content */}
        <div>
          <h2 className="text-white text-lg font-semibold">
            Work with the Rockets
          </h2>

          <p className="text-gray-200 text-sm mt-2 max-w-md">
            Wealth creation is an evolutionary recent positive-sum game.
            It is all about who take the opportunity first.
          </p>
        </div>

        
        <button className="text-white text-sm font-medium flex items-center gap-2 hover:gap-3 transition-all">
          Read more →
        </button>

      </div>
    </div>
  );
}
