const users = [
  { id: 1, name: "Aman Sharma", role: "Frontend Dev" },
  { id: 2, name: "Priya Singh", role: "Backend Dev" },
  { id: 3, name: "Rahul Verma", role: "UI Designer" },
  { id: 4, name: "Sneha Gupta", role: "Product Manager" },
  { id: 5, name: "Arjun Patel", role: "QA Engineer" },
];

export default function UserList() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      {users.map((user) => (
        <div
          key={user.id}
          className="bg-white p-4 rounded-xl shadow"
        >
          <h3 className="font-semibold">{user.name}</h3>
          <p className="text-gray-500 text-sm">{user.role}</p>
        </div>
      ))}
    </div>
  );
}
