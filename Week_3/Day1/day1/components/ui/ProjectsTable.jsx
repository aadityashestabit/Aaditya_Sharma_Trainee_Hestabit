import Image from "next/image";
import { HiDotsVertical } from "react-icons/hi";

const projects = [
  {
    name: "Chakra Soft UI Version",
    logo: "/images/1.png",
    budget: "$14,000",
    completion: 60,
  },
  {
    name: "Add Progress Track",
    logo: "/images/2.png",
    budget: "$3,000",
    completion: 10,
  },
  {
    name: "Fix Platform Errors",
    logo: "/images/3.png",
    budget: "Not set",
    completion: 100,
  },
  {
    name: "Launch our Mobile App",
    logo: "/images/4.png",
    budget: "$32,000",
    completion: 100,
  },
  {
    name: "Add the New Pricing Page",
    logo: "/images/5.png",
    budget: "$400",
    completion: 25,
  },
  {
    name: "Redesign New Online Shop",
    logo: "/images/6.png",
    budget: "$7,600",
    completion: 40,
  },
];

export default function ProjectsTable() {
  return (
    <div className="bg-[#FFFFFF] rounded-2xl p-6 shadow-sm flex-1 h-129.75">
      {/* Header */}
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2 className="text-lg font-semibold text-gray-800">Projects</h2>
          <p className="text-sm text-green-500 mt-1">
            ● <span className="text-gray-400">30 done this month</span>
          </p>
        </div>

        <HiDotsVertical className="text-gray-400 cursor-pointer" />
      </div>

      {/* Table Header */}
      <div className="grid grid-cols-4 text-xs font-semibold text-gray-400 pb-3 border-b">
        <p>COMPANIES</p>
        <p>MEMBERS</p>
        <p>BUDGET</p>
        <p>COMPLETION</p>
      </div>

      {/* Table Rows */}
      <div className="divide-y">
        {projects.map((project, index) => (
          <div key={index} className="grid grid-cols-4 items-center py-4">
            {/* Company */}
            <div className="flex items-center gap-3">
              <Image
                src={project.logo}
                alt={project.name}
                width={24}
                height={24}
                className="rounded-md object-contain"
              />

              <span className="text-sm font-medium text-gray-700">
                {project.name}
              </span>
            </div>

{/* Avatars */}
            <div className="flex -space-x-2">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="w-7 h-7 rounded-full border-2 border-white bg-gray-300"
                ></div>
              ))}
            </div>

            
            <p className="text-sm text-gray-700 font-medium">
              {project.budget}
            </p>

            
            <div>
              <p className="text-sm text-gray-700 font-medium mb-1">
                {project.completion}%
              </p>

              <div className="w-full h-1.5 bg-gray-200 rounded-full">
                <div
                  className="h-1.5 bg-[#4FD1C5] rounded-full"
                  style={{ width: `${project.completion}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
