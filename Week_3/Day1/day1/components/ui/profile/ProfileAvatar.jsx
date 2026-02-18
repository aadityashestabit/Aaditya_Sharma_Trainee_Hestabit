import Image from "next/image";

export default function ProfileAvatar({ image }) {
  return (
    <div className="relative ">
      <Image
        src={image}
        alt="Profile Avatar"
        width={70}
        height={70}
        className="rounded-2xl object-cover shadow-md"
      />
      <div className="absolute bottom-0 right-0 w-5 h-5 bg-white rounded-full flex items-center justify-center shadow">
        <div className="w-2.5 h-2.5 bg-teal-400 rounded-full"></div>
      </div>
    </div>
  );
}
