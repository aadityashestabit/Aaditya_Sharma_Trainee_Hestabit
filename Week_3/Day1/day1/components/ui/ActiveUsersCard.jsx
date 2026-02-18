import ActiveUsersChart from "./ActiveUsersChart";

export default function ActiveUsersCard() {
  const stats = [
    { label: "Users", value: "32,984", progress: "65%" },
    { label: "Clicks", value: "2,42m", progress: "80%" },
    { label: "Sales", value: "2,400$", progress: "40%" },
    { label: "Items", value: "320", progress: "60%" },
  ];

  return (
    <div className="bg-[#FFFFFF] rounded-2xl flex-1 h-111.25 max-w-5xl p-6 shadow-sm">
      
      {/* Import chart component */}
      <ActiveUsersChart />

      
      <div className="mt-6">
        
       
        <h2 className="text-lg font-semibold text-gray-800">
          Active Users
        </h2>

        <p className="text-sm mt-1">
          <span className="text-green-500 font-medium">(+23)</span>
          <span className="text-gray-400"> than last week</span>
        </p>

        
        <div className="grid grid-cols-4 gap-8 mt-6">
          {stats.map((item, index) => (
            <div key={index}>
              
            
              <p className="text-gray-400 text-sm font-medium">
                {item.label}
              </p>

            
              <p className="text-lg font-semibold text-gray-800 mt-2">
                {item.value}
              </p>

              
              <div className="w-full h-1 bg-gray-200 rounded-full mt-3">
                <div
                  className="h-1 bg-[#4FD1C5] rounded-full"
                  style={{ width: item.progress }}
                ></div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
