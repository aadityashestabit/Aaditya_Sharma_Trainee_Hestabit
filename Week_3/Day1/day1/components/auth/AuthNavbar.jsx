import Link from "next/link";

export default function AuthNavbar({buttonBg,textColor, buttonText,headingColor,bg}) {
  return (
    <div className="relative">
      <div className={`absolute left-1/2 -translate-x-1/2 top-10 z-10 
                      w-[60%] rounded-2xl px-10 py-4 
                      ${bg}  flex justify-between items-center`}>
        
        <h1 className={`font-semibold ${headingColor} text-sm`}>
          PURITY UI DASHBOARD
        </h1>

        <div className={`flex items-center gap-6 text-sm ${textColor} cursor-pointer`}>
          <Link 
href="/dashboard"


          ><span>Dashboard</span></Link>


          <span>Profile</span>
          <span>Sign Up</span>
          <span>Sign In</span>

          <button className={`${buttonBg} ${buttonText} px-4 py-1 rounded-full text-xs`}>
            Free Download
          </button>
        </div>

      </div>
    </div>
  );
}
