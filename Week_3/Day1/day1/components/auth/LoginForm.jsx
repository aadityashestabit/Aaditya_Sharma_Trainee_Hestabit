export default function LoginForm() {
  return (
    <div className="w-full flex flex-col justify-center items-center px-24">
      
      <h2 className="text-3xl font-semibold text-teal-500 mb-2">
        Welcome Back
      </h2>

      <p className="text-gray-400 text-sm mb-8">
        Enter your email and password to sign in
      </p>

      <div className="space-y-4 w-80">
        <div>
          <label className="text-xs text-gray-500">Email</label>
          <input
            type="email"
            placeholder="Your email address"
            className="w-full mt-1 px-4 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-teal-400"
          />
        </div>

        <div>
          <label className="text-xs text-gray-500">Password</label>
          <input
            type="password"
            placeholder="Your password"
            className="w-full mt-1 px-4 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-teal-400"
          />
        </div>

        <div className="flex items-center gap-2 text-xs text-gray-500">
          <input type="checkbox" />
          Remember me
        </div>

        <button className="w-full bg-teal-400 text-white py-2 rounded-xl text-sm font-semibold">
          SIGN IN
        </button>

        <p className="text-xs text-gray-400 text-center mt-4">
          Don't have an account?
          <span className="text-teal-500 ml-1 cursor-pointer">
            Sign up
          </span>
        </p>
      </div>
    </div>
  );
}
