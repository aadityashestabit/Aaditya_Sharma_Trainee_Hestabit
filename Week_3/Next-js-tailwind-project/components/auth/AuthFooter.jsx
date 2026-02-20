import Image from "next/image";

export default function AuthRightPanel() {
  return (
    <div className="w-1/2 relative">
      <Image
        src="/images/auth-bg.png"
        alt="Auth Background"
        fill
        className="object-cover rounded-l-3xl"
      />

      <div className="absolute inset-0 flex items-center justify-center">
        <h2 className="text-white text-4xl font-semibold">chakra</h2>
      </div>
    </div>
  );
}
