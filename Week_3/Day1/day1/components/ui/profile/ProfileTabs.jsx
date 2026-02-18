export default function ProfileTabs() {
  return (
    <div className="flex items-center gap-4">
      
      <button className="px-4 py-2 text-xs font-semibold bg-white rounded-full shadow-sm">
        OVERVIEW
      </button>

      <button className="px-4 py-2 text-xs text-gray-500 hover:text-gray-800">
        TEAMS
      </button>

      <button className="px-4 py-2 text-xs text-gray-500 hover:text-gray-800">
        PROJECTS
      </button>

    </div>
  );
}
