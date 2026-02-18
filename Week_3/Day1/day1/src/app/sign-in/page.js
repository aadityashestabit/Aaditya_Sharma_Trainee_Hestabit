import AuthNavbar from "../../../components/auth/AuthNavbar";
import LoginForm from "../../../components/auth/LoginForm";
import AuthRightPanel from "../../../components/auth/AuthRightPanel";
import AuthFooter from "../../../components/auth/AuthFooter";
import Footer from "../../../components/ui/Footer";

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      
      <AuthNavbar buttonBg="bg-gray-800"
      headingColor="text-gray-800"
      textColor="text-gray-600"
      buttonText="text-white"
      bg="bg-white"
      />

      <div className="flex flex-1">
        <LoginForm />
        <AuthRightPanel />
      </div>

      <div className="px-60 py-4">
        <Footer/>
      </div>

    </div>
  );
}
