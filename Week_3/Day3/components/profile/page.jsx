import Image from "next/image";
import ProfileHeader from "../../../components/profile/ProfileHeader";
import ProfileNavbar from "../../../components/profile/ProfileNavbar";
import PlatformSettings from "../../../components/profile/PlatformSettings";
import ProfileInformation from "../../../components/profile/ProfileInformation";
import Conversation from "../../../components/profile/Conversation";
import Footer from "../../../components/ui/Footer";

export default function Profile() {
  return (
    <div className="relative min-h-screen p-6">
      <div className="relative h-75 w-full">
        {/* Background Image */}
        <Image
          src="/images/profile_background.png"
          alt="Profile Background"
          width={1598}
          height={300}
          className="w-full object-cover"
        />
        {/* Profile Header */}
        <div className="absolute left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90%]">
          <ProfileHeader />
        </div>

        <div className="absolute top-0 left-0 w-full z-20">
          <ProfileNavbar pageName="Profile" />
        </div>
      </div>

      <div className="flex gap-4">
        <div>
          <PlatformSettings />
        </div>

        <div>
          <ProfileInformation />
        </div>

        <div>
          <Conversation />
        </div>
      </div>

      <div>
        <Footer />
      </div>
    </div>
  );
}
