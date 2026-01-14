"use client";

import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import {
  LogIn,
  Loader2,
  Lock,
  User,
  Database,
  ShieldCheck,
  Sparkles,
  ChevronRight,
  Server,
  Layers,
  Key,
  Cpu,
  Zap,
  Globe,
  Shield,
  Terminal,
  Activity,
} from "lucide-react";

export default function LoginPage() {
  const { login, isLoading } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [useAdmin, setUseAdmin] = useState(false);

  // Database-themed background images
  const backgroundImages = [
    "https://images.unsplash.com/photo-1547658719-da2b51169166?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80", // Server room
    "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80", // Data center
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80", // Network cables
  ];

  const [currentImage] = useState(backgroundImages[0]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const creds = useAdmin
      ? { username: "superadmin", password: "Admin123!" }
      : username.includes("manager")
      ? { username, password: "Manager123!" }
      : { username, password };

    if (!creds.username || !creds.password) {
      toast.error("Please fill in all fields");
      return;
    }

    try {
      await login(creds.username, creds.password);
      toast.success("Authentication successful! Access granted.");
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Authentication failed. Invalid credentials."
      );
    }
  };

  const handleDemoLogin = (role: "admin" | "manager" | "user") => {
    switch (role) {
      case "admin":
        setUseAdmin(true);
        setUsername("superadmin");
        setPassword("Admin123!");
        toast.info("Superadmin credentials loaded", {
          description: "Full system access with all permissions",
        });
        break;
      case "manager":
        setUseAdmin(false);
        setUsername("alice_manager");
        setPassword("Manager123!");
        toast.info("Manager credentials loaded", {
          description: "Manage users, products, and inventory",
        });
        break;
      case "user":
        setUseAdmin(false);
        setUsername("john_user");
        setPassword("User123!");
        toast.info("User credentials loaded", {
          description: "View products and manage own content",
        });
        break;
    }
  };

  // Floating database particles
  const DatabaseParticles = () => (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(15)].map((_, i) => (
        <div
          key={i}
          className="absolute animate-float"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${15 + Math.random() * 20}s`,
          }}
        >
          <Database className="h-3 w-3 text-primary-blue/30" />
        </div>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen">
      <div className="grid grid-cols-1 lg:grid-cols-7 min-h-screen">
        {/* Left Column - Full Image Background */}
        <div className="lg:col-span-2 relative overflow-hidden">
          {/* Background Image */}
          <div
            className="absolute inset-0 bg-cover bg-center"
            style={{
              backgroundImage: `url('${currentImage}')`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              filter: "brightness(0.4)",
            }}
          />
        </div>

        {/* Right Column - Login Form */}
        <div className="lg:col-span-5 flex items-center justify-center p-4 md:p-8 lg:p-12">
          <div className="w-full max-w-xl">
            <Card className="border-none shadow-none">
              <CardHeader className="space-y-2">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-primary-blue/10 rounded-lg">
                    <Key className="h-6 w-6 text-primary-blue" />
                  </div>
                  <div>
                    <CardTitle className="text-gray-900">
                      Access Console
                    </CardTitle>
                    <CardDescription className="text-gray-600">
                      Authenticate to manage database resources
                    </CardDescription>
                  </div>
                </div>

                {/* Security Status */}
                <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-emerald-50 to-emerald-100 rounded-full border border-emerald-200">
                  <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span className="text-xs text-emerald-700 font-medium">
                    Secure Connection Active
                  </span>
                </div>
              </CardHeader>

              <CardContent className="space-y-6">
                <form onSubmit={handleSubmit} className="space-y-5">
                  {/* Username Field */}
                  <div className="space-y-3">
                    <Label htmlFor="username" className="text-gray-700">
                      Database Username
                    </Label>
                    <div className="relative group">
                      <div className="absolute left-3 top-1/2 -translate-y-1/2">
                        <User className="h-5 w-5 text-gray-400 group-focus-within:text-primary-blue transition-colors" />
                      </div>
                      <Input
                        id="username"
                        value={username}
                        onChange={(e) => {
                          setUsername(e.target.value);
                          if (useAdmin) setUseAdmin(false);
                        }}
                        placeholder="Enter database username"
                        disabled={isLoading || useAdmin}
                        className="pl-10 bg-white border-gray-300 text-gray-900 placeholder:text-gray-500 focus:border-primary-blue focus:ring-primary-blue/30"
                      />
                      {username && !useAdmin && (
                        <div className="absolute right-3 top-1/2 -translate-y-1/2">
                          <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Password Field */}
                  <div className="space-y-3">
                    <Label htmlFor="password" className="text-gray-700">
                      Database Password
                    </Label>
                    <div className="relative group">
                      <div className="absolute left-3 top-1/2 -translate-y-1/2">
                        <Lock className="h-5 w-5 text-gray-400 group-focus-within:text-primary-blue transition-colors" />
                      </div>
                      <Input
                        id="password"
                        type="password"
                        value={password}
                        onChange={(e) => {
                          setPassword(e.target.value);
                          if (useAdmin) setUseAdmin(false);
                        }}
                        placeholder="Enter your secure password"
                        disabled={isLoading || useAdmin}
                        className="pl-10 bg-white border-gray-300 text-gray-900 placeholder:text-gray-500 focus:border-primary-blue focus:ring-primary-blue/30"
                      />
                    </div>
                  </div>

                  {/* Admin Toggle */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="admin"
                        checked={useAdmin}
                        onCheckedChange={(checked) => {
                          setUseAdmin(checked === true);
                          if (checked) handleDemoLogin("admin");
                        }}
                        className="data-[state=checked]:bg-primary-blue border-gray-300"
                      />
                      <Label
                        htmlFor="admin"
                        className="text-sm font-medium text-gray-700"
                      >
                        Superadmin Mode
                      </Label>
                    </div>

                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="text-primary-blue hover:text-primary-blue/80 hover:bg-primary-blue/10 text-xs"
                    >
                      <ShieldCheck className="h-3 w-3 mr-1" />
                      Security Info
                    </Button>
                  </div>

                  {/* Quick Access Buttons */}
                  <div className="space-y-3">
                    <p className="text-sm text-gray-600 font-medium">
                      Quick Access Profiles:
                    </p>
                    <div className="grid grid-cols-3 gap-2">
                      <Button
                        type="button"
                        variant={useAdmin ? "default" : "outline"}
                        size="sm"
                        onClick={() => handleDemoLogin("admin")}
                        className={`gap-2 transition-all ${
                          useAdmin
                            ? "bg-gradient-to-r from-primary-blue to-cyan-600 border-primary-blue shadow-lg shadow-primary-blue/30 text-white"
                            : "border-gray-300 bg-white text-gray-700 hover:border-primary-blue hover:bg-primary-blue/5"
                        }`}
                      >
                        <Cpu className="h-3 w-3" />
                        Admin
                      </Button>
                      <Button
                        type="button"
                        variant={
                          username.includes("manager") && !useAdmin
                            ? "default"
                            : "outline"
                        }
                        size="sm"
                        onClick={() => handleDemoLogin("manager")}
                        className={`gap-2 transition-all ${
                          username.includes("manager") && !useAdmin
                            ? "bg-gradient-to-r from-primary-blue to-cyan-600 border-primary-blue shadow-lg shadow-primary-blue/30 text-white"
                            : "border-gray-300 bg-white text-gray-700 hover:border-primary-blue hover:bg-primary-blue/5"
                        }`}
                      >
                        <Layers className="h-3 w-3" />
                        Manager
                      </Button>
                      <Button
                        type="button"
                        variant={
                          username.includes("user") && !useAdmin
                            ? "default"
                            : "outline"
                        }
                        size="sm"
                        onClick={() => handleDemoLogin("user")}
                        className={`gap-2 transition-all ${
                          username.includes("user") && !useAdmin
                            ? "bg-gradient-to-r from-primary-blue to-cyan-600 border-primary-blue shadow-lg shadow-primary-blue/30 text-white"
                            : "border-gray-300 bg-white text-gray-700 hover:border-primary-blue hover:bg-primary-blue/5"
                        }`}
                      >
                        <User className="h-3 w-3" />
                        User
                      </Button>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    className="w-full group mt-6 bg-gradient-to-r from-primary-blue to-primary-dark hover:from-primary-blue/90 hover:to-primary-dark/90 text-white shadow-xl shadow-primary-blue/20 transition-all duration-300 hover:scale-[1.02]"
                    disabled={isLoading}
                    size="lg"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Establishing Secure Connection...
                      </>
                    ) : (
                      <>
                        <Zap className="mr-2 h-4 w-4 group-hover:animate-pulse" />
                        <span>Authenticate & Connect</span>
                        <ChevronRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                      </>
                    )}
                  </Button>
                </form>

                {/* Security Features */}
                <div className="pt-4 border-t border-gray-200 space-y-4">

                  <div className="bg-gradient-to-r from-gray-50 to-primary-blue/5 rounded-lg p-3 border border-gray-200">
                    <div className="flex items-start gap-2">
                      <Terminal className="h-4 w-4 text-primary-blue mt-0.5" />
                      <div>
                        <p className="text-xs text-gray-600">
                          All database operations are logged. Unauthorized
                          access attempts will trigger security protocols.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

          </div>
        </div>
      </div>

      {/* Global Styles for Animations */}
      <style jsx global>{`
        @keyframes float {
          0%,
          100% {
            transform: translateY(0) rotate(0deg);
          }
          50% {
            transform: translateY(-20px) rotate(5deg);
          }
        }
        .animate-float {
          animation: float infinite ease-in-out;
        }
      `}</style>
    </div>
  );
}
