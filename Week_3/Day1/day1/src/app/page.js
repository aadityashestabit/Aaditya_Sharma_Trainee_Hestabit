import Navbar from "../../components/ui/Navbar";
import StatCard from "../../components/ui/Statcard";
import { IoWallet } from "react-icons/io5";
import { LuGlobe } from "react-icons/lu";
import { FaFile } from "react-icons/fa6";
import Promobanner from "../../components/ui/Promobanner";
import RocketCard from "../../components/ui/RocketCard";
import ActiveUsersCard from "../../components/ui/ActiveUsersCard";
import SalesOverviewChart from "../../components/ui/SalesOverViewChart";
import ProjectsTable from "../../components/ui/ProjectsTable";
import Footer from "../../components/ui/Footer";

export default function Home() {
  return (
    <>
      {/* <Navbar /> */}
      <div className="flex gap-2 p-4">
        <StatCard 
        icon={<IoWallet size={20} color="white"/>}
        label="Today's Money" 
        amount="53,000"
        percentage="+55"
        />

        <StatCard 
        icon={<LuGlobe size={20} color="white"/>}
        label="Today's Users" 
        amount="2,300"
        percentage="+5"
        />

        <StatCard 
        icon={<FaFile size={20} color="white"/>}
        label="New Clients" 
        amount="+3,051"
        percentage="-14"
        />
        
      </div>

      <div className="p-4 flex gap-2">
      <Promobanner />
      <RocketCard/>

    </div>

    <div className="p-4 flex gap-7">
      <ActiveUsersCard/>
      <SalesOverviewChart/>
    </div>

    <div className="p-4">
      <ProjectsTable/>
    </div>

    <Footer/>
    </>
  );
}
