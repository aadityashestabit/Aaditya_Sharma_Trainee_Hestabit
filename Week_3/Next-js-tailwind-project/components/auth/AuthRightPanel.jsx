import { AiFillThunderbolt } from "react-icons/ai";
export default function AuthRightPanel() {
  return (
    <div className="min-w-[40%] h-160 relative overflow-hidden ml-auto rounded-bl-3xl bg-linear-to-br from-teal-400 to-teal-600 flex items-center justify-center">
      {/* Centering the content  */}
      <div className="relative text-white flex items-center gap-4">
        {/* Chakra icon  */}
        <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold">
          <AiFillThunderbolt color="white" size={30} />
        </div>

        <h2 className="text-4xl font-semibold tracking-wide">chakra</h2>
      </div>
    </div>
  );
}
