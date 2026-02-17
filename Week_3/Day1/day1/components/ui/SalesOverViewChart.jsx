"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const data = [
  { month: "Jan", uv: 500, pv: 180 },
  { month: "Feb", uv: 180, pv: 160 },
  { month: "Mar", uv: 210, pv: 200 },
  { month: "Apr", uv: 350, pv: 270 },
  { month: "May", uv: 370, pv: 210 },
  { month: "Jun", uv: 470, pv: 230 },
  { month: "Jul", uv: 440, pv: 250 },
  { month: "Aug", uv: 310, pv: 210 },
  { month: "Sep", uv: 360, pv: 110 },
  { month: "Oct", uv: 220, pv: 140 },
  { month: "Nov", uv: 400, pv: 170 },
  { month: "Dec", uv: 430, pv: 130 },
];

export default function SalesOverviewChart() {
  return (
    <div className="bg-[#FFFFFF] rounded-2xl p-6 shadow-sm flex-1 h-111.25">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-800">Sales overview</h2>
        <p className="text-sm mt-1">
          <span className="text-green-500 font-medium">(+5)</span>
          <span className="text-gray-400"> more in 2021</span>
        </p>
      </div>

      {/* Chart */}
      <div className="h-75">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <CartesianGrid
              strokeDasharray="4 4"
              vertical={false}
              stroke="#E2E8F0"
            />

            <XAxis
              dataKey="month"
              tick={{ fontSize: 12, fill: "#A0AEC0" }}
              axisLine={false}
              tickLine={false}
            />

            <YAxis
              domain={[0, 500]}
              ticks={[0, 100, 200, 300, 400, 500]}
              tick={{ fontSize: 12, fill: "#A0AEC0" }}
              axisLine={false}
              tickLine={false}
            />

            <Area
              type="monotone"
              dataKey="uv"
              stroke="#4FD1C5"
              fill="#4FD1C5"
              fillOpacity={0.25}
              strokeWidth={3}
            />

            <Area
              type="monotone"
              dataKey="pv"
              stroke="#2D3748"
              fill="transparent"
              strokeWidth={3}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
