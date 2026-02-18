import Image from "next/image";

export default function ConversationTile({
  image,
  name,
  message,
}) {
  return (
<div>
    

    <div className="flex items-center justify-between bg-white rounded-xl p-2 ">

        
      
      {/* Left Section */}
      <div className="flex items-center gap-3">
        
        {/* Avatar */}
        <Image
          src={image}
          alt={name}
          width={50}
          height={50}
          className="rounded-2xl object-cover"
        />

        {/* Text */}
        <div>
          <h3 className="text-sm font-semibold text-gray-800">
            {name}
          </h3>
          <p className="text-sm text-gray-400">
            {message}
          </p>
        </div>
      </div>

      {/* Right Section */}
      <button
        className="text-xs font-semibold text-teal-400 hover:text-teal-500 transition"
      >
        REPLY
      </button>

    </div>
    </div>
  );
}
