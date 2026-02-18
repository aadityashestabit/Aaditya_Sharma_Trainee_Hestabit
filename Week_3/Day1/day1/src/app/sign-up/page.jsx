import Image from "next/image";
import AuthNavbar from "../../../components/auth/AuthNavbar";
import RegisterCard from "../../../components/ui/signup/RegisterCard";
import Footer from "../../../components/ui/Footer";

export default function SignUpPage() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      {/* HERO SECTION */}
      <div className="relative h-[420px] w-full rounded-b-3xl overflow-hidden">
        
        {/* Background Image */}
        <Image
          src="/images/SignUp_Banner.png" 
          alt="Hero Background"
          fill
          priority
          className="object-cover"
        />

        {/* Optional Overlay (for readability) */}
        <div className="absolute"></div>

        {/* Navbar Over Image */}
        <div className="absolute top-0 left-0 w-full z-20">
          <AuthNavbar
          buttonBg="bg-[#FFFFFF]"
          headingColor="text-[#FFFFFF]"
          textColor="text-[#FFFFFF]"
          buttonText="text-gray-900"
          bg="bg-transparent"
          />
        </div>

        {/* Center Welcome Text */}
        <div className="relative z-20 flex flex-col items-center justify-center h-full text-white text-center space-y-4">
          <h1 className="text-3xl font-semibold">Welcome!</h1>
          <p className="text-sm max-w-md opacity-90">
            Use these awesome forms to login or create new
            account in your project for free.
          </p>
        </div>
      </div>

      {/* REGISTER CARD */}
      <div className="relative flex justify-center -mt-24 z-30">
        <RegisterCard />
      </div>

      {/* FOOTER */}
      <Footer/>

    </div>
  );
}
