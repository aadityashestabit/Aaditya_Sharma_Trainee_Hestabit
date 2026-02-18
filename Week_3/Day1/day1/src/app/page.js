import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      
      <div className="text-center space-y-6">
        
        <h1 className="text-3xl font-semibold text-gray-800">
          Welcome to Dashboard App
        </h1>

        <Link href="/dashboard">
          <button className="px-6 py-3 bg-teal-500 text-white rounded-xl font-medium hover:bg-teal-600 transition">
            Go to Dashboard
          </button>
        </Link>

      </div>

    </div>
  );
}
