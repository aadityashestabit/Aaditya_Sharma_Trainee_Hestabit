"use client";

import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from "recharts";

const data = [
  { value: 320 },
  { value: 220 },
  { value: 120 },
  { value: 280 },
  { value: 500 },
  { value: 420 },
  { value: 470 },
  { value: 290 },
  { value: 160 },
];

export default function ActiveUsersChart() {
  return (
    <div className="bg-linear-to-r from-[#313860] to-[#151928] rounded-2xl p-6 h-55">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <YAxis
            stroke="#A0AEC0"
            tick={{ fontSize: 12 }}
            axisLine={false}
            tickLine={false}
          />

          <XAxis hide />

          <Bar
            dataKey="value"
            fill="#FFFFFF"
            radius={[10, 10, 10, 10]}
            barSize={8}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
