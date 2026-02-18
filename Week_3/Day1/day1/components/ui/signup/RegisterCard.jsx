"use client";

import { useState } from "react";
import { FaFacebookF, FaApple, FaGoogle } from "react-icons/fa";

export default function RegisterCard() {
  const [remember, setRemember] = useState(true);

  return (
    <div className="w-full max-w-md bg-white rounded-2xl shadow-sm p-8 space-y-4">
      
      {/* Title */}
      <h2 className="text-center text-sm font-semibold text-gray-600">
        Register with
      </h2>

      {/* Social Buttons */}
      <div className="flex justify-center gap-4">
        <button className="w-12 h-12 rounded-xl border border-gray-200 flex items-center justify-center text-gray-600 hover:bg-gray-50 transition">
          <FaFacebookF />
        </button>

        <button className="w-12 h-12 rounded-xl border border-gray-200 flex items-center justify-center text-gray-600 hover:bg-gray-50 transition">
          <FaApple />
        </button>

        <button className="w-12 h-12 rounded-xl border border-gray-200 flex items-center justify-center text-gray-600 hover:bg-gray-50 transition">
          <FaGoogle />
        </button>
      </div>

      {/* Divider */}
      <div className="flex items-center gap-4">
        <div className="flex-1 h-px bg-gray-200"></div>
        <span className="text-xs text-gray-400">or</span>
        <div className="flex-1 h-px bg-gray-200"></div>
      </div>

      {/* Name */}
      <div>
        <label className="text-xs font-semibold text-gray-500">
          Name
        </label>
        <input
          type="text"
          placeholder="Your full name"
          className="w-full mt-1 px-4 py-2.5 text-sm border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-teal-400"
        />
      </div>

      {/* Email */}
      <div>
        <label className="text-xs font-semibold text-gray-500">
          Email
        </label>
        <input
          type="email"
          placeholder="Your email address"
          className="w-full mt-1 px-4 py-2.5 text-sm border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-teal-400"
        />
      </div>

      {/* Password */}
      <div>
        <label className="text-xs font-semibold text-gray-500">
          Password
        </label>
        <input
          type="password"
          placeholder="Your password"
          className="w-full mt-1 px-4 py-2.5 text-sm border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-teal-400"
        />
      </div>

      {/* Remember Me Toggle */}
      <div className="flex items-center gap-3 text-xs text-gray-500">
        <button
          onClick={() => setRemember(!remember)}
          className={`relative w-10 h-5 rounded-full transition ${
            remember ? "bg-teal-400" : "bg-gray-300"
          }`}
        >
          <span
            className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition ${
              remember ? "translate-x-5" : ""
            }`}
          />
        </button>
        Remember me
      </div>

      {/* Sign Up Button */}
      <button className="w-full bg-teal-400 hover:bg-teal-500 transition text-white py-2.5 rounded-xl text-sm font-semibold">
        Sign up
      </button>

      {/* Footer */}
      <p className="text-center text-xs text-gray-400">
        Already have an account?{" "}
        <span className="text-teal-400 font-medium cursor-pointer hover:underline">
          Sign in
        </span>
      </p>

    </div>
  );
}
