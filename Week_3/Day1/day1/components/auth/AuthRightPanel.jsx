import { AiFillThunderbolt } from "react-icons/ai";
export default function AuthRightPanel() {
  return (
    <div className="min-w-[40%] h-160 relative overflow-hidden ml-auto rounded-bl-3xl bg-linear-to-br from-teal-400 to-teal-600 flex items-center justify-center">
      
      {/* Soft Abstract Circles */}
      <div className="absolute w-96 h-96 bg-white/10 rounded-full -top-20 -right-20 blur-2xl"></div>
      <div className="absolute w-72 h-72 bg-white/10 rounded-full bottom-10 left-10 blur-2xl"></div>
      <div className="absolute w-80 h-80 bg-white/5 rounded-full top-40 left-40 blur-3xl"></div>

      {/* Center Content */}
      <div className="relative text-white flex items-center gap-4">
        
        {/* Simple Chakra Icon Circle */}
        <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center text-2xl font-bold">
          <AiFillThunderbolt color="white" size={30}/>
        </div>

        <h2 className="text-4xl font-semibold tracking-wide">
          chakra
        </h2>
      </div>

    </div>
  );
}
