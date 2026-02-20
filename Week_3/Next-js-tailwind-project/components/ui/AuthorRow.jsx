import Image from "next/image";

export default function AuthorRow({ author }) {
  return (
    <div className="grid grid-cols-5 items-center py-3 text-gray-300 border-b last:border-none">
      <div className="flex items-center gap-3">
        <Image
          src={author.image}
          alt={author.name}
          width={40}
          height={40}
          className="rounded-xl object-cover"
        />
        <div>
          <p className="text-sm font-semibold text-gray-800">{author.name}</p>
          <p className="text-xs text-gray-400">{author.email}</p>
        </div>
      </div>

      <div>
        <p className="text-sm font-semibold text-gray-700">{author.role}</p>
        <p className="text-xs text-gray-400">{author.department}</p>
      </div>

      <div>
        <span
          className={`px-3 py-1 text-xs font-medium rounded-full ${
            author.status === "Online"
              ? "bg-green-100 text-green-600"
              : "bg-gray-200 text-gray-500"
          }`}
        >
          {author.status}
        </span>
      </div>

      <p className="text-sm text-gray-600">{author.date}</p>

      <button className="text-sm text-gray-500 hover:text-gray-800">
        Edit
      </button>
    </div>
  );
}
