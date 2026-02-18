import { FaFacebookF, FaTwitter, FaInstagram } from "react-icons/fa";

export default function ProfileInformation() {
  return (
    <div className="w-full max-w-sm max-h-110 h-full bg-white rounded-2xl p-8 space-y-6">
      
      {/* Title */}
      <h2 className="text-lg font-semibold text-gray-800">
        Profile Information
      </h2>

      {/* Description */}
      <p className="text-sm text-gray-400 leading-relaxed">
        Hi, I’m Alec Thompson, Decisions: If you can’t decide, the answer is no.
        If two equally difficult paths, choose the one more painful in the short
        term (pain avoidance is creating an illusion of equality).
      </p>

      {/* Divider */}
      <div className="border-t border-gray-200"></div>

      {/* Info List */}
      <div className="space-y-4 text-sm">
        
        <InfoRow label="Full Name" value="Alec M. Thompson" />
        <InfoRow label="Mobile" value="(44) 123 1234 123" />
        <InfoRow label="Email" value="alecthompson@mail.com" />
        <InfoRow label="Location" value="United States" />

        {/* Social Media */}
        <div className="flex items-center gap-4">
          <span className="font-semibold text-gray-600 w-28">
            Social Media:
          </span>

          <div className="flex gap-4 text-teal-400 text-sm">
            <FaFacebookF className="cursor-pointer hover:scale-110 transition" />
            <FaTwitter className="cursor-pointer hover:scale-110 transition" />
            <FaInstagram className="cursor-pointer hover:scale-110 transition" />
          </div>
        </div>

      </div>
    </div>
  );
}


/* Reusable Row Component */
function InfoRow({ label, value }) {
  return (
    <div className="flex">
      <span className="font-semibold text-gray-600 w-28">
        {label}:
      </span>
      <span className="text-gray-500">
        {value}
      </span>
    </div>
  );
}
