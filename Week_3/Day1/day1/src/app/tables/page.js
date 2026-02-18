import AuthorsTable from "../../../components/ui/AuthorsTable";
import Footer from "../../../components/ui/Footer";
import Navbar from "../../../components/ui/Navbar";
import ProjectsTable from "../../../components/ui/ProjectsTable";

export default function Table() {
  return (
    <>
      <div className="p-4">
        <AuthorsTable />
      </div>

      <div className="p-4">
        <ProjectsTable/>
      </div>

      <Footer/>
    </>
  );
}
