import ProfileAvatar from "./ProfileAvatar";
import ProfileTabs from "./ProfileTabs";

export default function ProfileHeader() {
  return (
    <div className="bg-white/80 h-25 rounded-2xl p-8  flex justify-between items-center">
      {/* Left Section */}
      <div className="flex items-center gap-4">
        <ProfileAvatar image="/images/3_face.png" />

        <div>
          <h2 className="text-lg font-semibold text-gray-800">
            Esthera Jackson
          </h2>
          <p className="text-sm text-gray-500">esthera@simmmple.com</p>
        </div>
      </div>

      {/* Right Section */}
      <ProfileTabs />
    </div>
  );
}
