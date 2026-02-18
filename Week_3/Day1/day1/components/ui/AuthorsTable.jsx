import AuthorRow from "./AuthorRow";

const authors = [
  {
    name: "Esthera Jackson",
    email: "esthera@simmmple.com",
    image: "/images/1_face.png",
    role: "Manager",
    department: "Organization",
    status: "Online",
    date: "14/06/21",
  },
  {
    name: "Alexa Liras",
    email: "alexa@simmmple.com",
    image: "/images/2_face.png",
    role: "Programmer",
    department: "Developer",
    status: "Offline",
    date: "14/06/21",
  },
  {
    name: "Laurent Michael",
    email: "laurent@simmmple.com",
    image: "/images/3_face.png",
    role: "Executive",
    department: "Projects",
    status: "Online",
    date: "14/06/21",
  },
  {
    name: "Freduardo Hill",
    email: "freduardo@simmmple.com",
    image: "/images/4_face.png",
    role: "Manager",
    department: "Organization",
    status: "Online",
    date: "14/06/21",
  },
  {
    name: "Daniel Thomas",
    email: "daniel@simmmple.com",
    image: "/images/5_face.png",
    role: "Programmer",
    department: "Developer",
    status: "Offline",
    date: "14/06/21",
  },
  {
    name: "Mark Wilson",
    email: "mark@simmmple.com",
    image: "/images/6_face.png",
    role: "Designer",
    department: "UI/UX Design",
    status: "Offline",
    date: "14/06/21",
  },
];

export default function AuthorsTable() {
  return (
    <div className="bg-[#F8F9FA] rounded-2xl p-4  shadow-sm  w-full">
      
      <h2 className="text-lg font-semibold text-gray-800 mb-3">
        Authors Table
      </h2>

      {/* Header Row */}
      <div className="grid grid-cols-5 text-xs font-semibold text-gray-400 pb-3 border-b">
        <p>AUTHOR</p>
        <p>FUNCTION</p>
        <p>STATUS</p>
        <p>EMPLOYED</p>
        <p></p>
      </div>

      {/* Rows */}
      <div>
        {authors.map((author, index) => (
          <AuthorRow key={index} author={author} />
        ))}
      </div>

    </div>
  );
}
