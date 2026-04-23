import Sidebar from "../../../components/ui/Sidebar";

export default function Layout({ children }) {
  return (
    <div className="flex bg-gray-100 min-h-screen">
      <Sidebar />

      <main className="flex flex-col flex-1">{children}</main>
    </div>
  );
}
