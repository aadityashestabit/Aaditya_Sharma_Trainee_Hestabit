export default function Footer() {
  return (
    <footer className="w-full px-6 py-4 ">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium">
          &copy; Made with ❤️ by <span className="text-green-500">Aaditya</span>
        </span>

        <ul className="flex gap-6 text-gray-400 text-sm font-medium cursor-pointer">
          <li>Creative</li>
          <li>Simple</li>
          <li>Contact</li>
          <li>License</li>
        </ul>
      </div>
    </footer>
  );
}
