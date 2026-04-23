import Image from "next/image";
import AuthNavbar from "../../../components/auth/AuthNavbar";
import RegisterCard from "../../../components/signup/RegisterCard";
import Footer from "../../../components/ui/Footer";

export default function SignUpPage() {
  return (
    <div className="min-h-screen bg-gray-100 p-3 flex flex-col">
      <div className="relative h-105 w-full rounded-xl overflow-hidden">
        {/* Background Image */}
        <Image
          src="/images/SignUp_Banner.png"
          alt="Hero Background"
          fill
          priority
          className="object-cover"
        />

        <div className="absolute"></div>

        {/* Navbar Over Image */}
        <div className="absolute top-0 left-0 w-full z-100">
          <AuthNavbar
            buttonBg="bg-[#FFFFFF]"
            headingColor="text-[#FFFFFF]"
            textColor="text-[#FFFFFF]"
            buttonText="text-gray-900"
            bg="bg-transparent"
          />
        </div>

        <div className="relative z-20 flex flex-col items-center justify-center h-full text-white text-center space-y-2">
          <h1 className="text-3xl font-semibold">Welcome!</h1>
          <p className="text-sm max-w-md opacity-90">
            Use these awesome forms to login or create new account in your
            project for free.
          </p>
        </div>
      </div>

      <div className="relative flex justify-center -mt-35 z-30">
        <RegisterCard />
      </div>

      <Footer />
    </div>
  );
}
