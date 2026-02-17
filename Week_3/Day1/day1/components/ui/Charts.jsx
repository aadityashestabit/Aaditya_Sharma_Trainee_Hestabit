"use client";

import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "Jan", users: 30, sales: 400 },
  { name: "Feb", users: 45, sales: 300 },
  { name: "Mar", users: 60, sales: 500 },
  { name: "Apr", users: 40, sales: 350 },
  { name: "May", users: 80, sales: 600 },
];

export default function Charts() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Area Chart */}
      <div className="bg-white p-4 rounded-xl shadow h-72">
        <h3 className="mb-4 font-semibold">User Growth</h3>
        <ResponsiveContainer width="100%" height="85%">
          <AreaChart data={data}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="users"
              stroke="#6366F1"
              fill="#6366F1"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Bar Chart */}
      <div className="bg-white p-4 rounded-xl shadow h-72">
        <h3 className="mb-4 font-semibold">Sales</h3>
        <ResponsiveContainer width="100%" height="85%">
          <BarChart data={data}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="sales" fill="#10B981" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
