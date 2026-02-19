import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-linear-to-br from-gray-100 relative to-gray-200 flex flex-col">
      <div className="absolute w-40 h-40 bg-black/4 rounded-full top-40 left-20"></div>
      <div className="absolute w-32 h-32 bg-black/7 rounded-full bottom-50 left-10"></div>

      <div className="absolute w-40 h-40 bg-black/5 rounded-full top-60 left-120"></div>
      <div className="absolute w-32 h-32 bg-black/4 rounded-full bottom-80 left-230"></div>

      <div className="absolute w-40 h-40 bg-black/7 rounded-full top-50 left-190"></div>
      <div className="absolute w-32 h-32 bg-black/4 rounded-full top-30 left-280"></div>

      <nav className="flex justify-between items-center px-10 py-6">
        <h1 className="text-lg font-bold text-gray-800">PURITY UI</h1>

        <Link href="/dashboard">
          <button className="px-5 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition">
            Dashboard
          </button>
        </Link>
      </nav>

      <div className="flex-1 flex flex-col items-center justify-center text-center px-6">
        <h2 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
          Build Modern Admin Dashboards
        </h2>

        <p className="text-gray-600 max-w-xl mb-8">
          A clean and scalable dashboard UI built with Next.js and Tailwind CSS.
          Designed for speed, simplicity and professional SaaS applications.
        </p>

        <Link href="/dashboard">
          <button className="px-8 py-3 bg-teal-500 text-white rounded-xl font-medium text-lg shadow-md hover:shadow-lg hover:bg-teal-600 transition-all duration-200">
            Get Started
          </button>
        </Link>
      </div>

      <footer className="text-center text-sm text-gray-500 py-6">
        &copy; 2026 Purity UI Dashboard. All rights reserved.
      </footer>
    </div>
  );
}
