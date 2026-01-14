// src/app/(dashboard)/profile/page.tsx
"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  User,
  Key,
  Calendar,
  Mail,
  Shield,
  Lock,
  LogOut,
  UserCircle,
  Activity,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";
import { toast } from "sonner";

export default function ProfilePage() {
  const { user } = useAuth();
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [activeTab, setActiveTab] = useState("profile");

  const handlePasswordChange = (e: React.FormEvent) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      toast.error("New passwords do not match");
      return;
    }

    if (newPassword.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }

    toast.success("Password changed successfully (demo)");
    setOldPassword("");
    setNewPassword("");
    setConfirmPassword("");
  };

  const handleLogoutAll = () => {
    toast.success("Logged out from all devices (demo)");
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Profile Settings</h1>
        <p className="text-gray-600 mt-2">
          Manage your account and preferences
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <Card className="border-none shadow-none bg-gray-50">
            <CardContent className="p-6">
              <div className="flex flex-col items-center space-y-4">
                <div className="relative">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary-blue to-primary-dark flex items-center justify-center">
                    <UserCircle className="h-12 w-12 text-white" />
                  </div>
                  <div className="absolute bottom-0 right-0 h-6 w-6 rounded-full bg-green-500 border-2 border-white"></div>
                </div>
                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {user?.username}
                  </h3>
                  <p className="text-sm text-gray-600">{user?.email}</p>
                  <Badge className="mt-2 bg-primary-blue text-white">
                    {user?.role_name}
                  </Badge>
                </div>
                <Separator />
                <div className="text-sm text-gray-500 space-y-1">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    <span>
                      Joined{" "}
                      {user?.created_at
                        ? new Date(user.created_at).toLocaleDateString(
                            "en-US",
                            {
                              month: "long",
                              year: "numeric",
                            }
                          )
                        : ""}
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          <Tabs
            value={activeTab}
            onValueChange={setActiveTab}
            className="space-y-6"
          >
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="profile" className="flex items-center gap-2">
                <User className="h-4 w-4" />
                Profile
              </TabsTrigger>
              <TabsTrigger value="security" className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Security
              </TabsTrigger>
              <TabsTrigger value="activity" className="flex items-center gap-2">
                <Activity className="h-4 w-4" />
                Activity
              </TabsTrigger>
            </TabsList>

            {/* Profile Tab */}
            <TabsContent value="profile" className="space-y-6">
              <Card className="border-none shadow-none">
                <CardHeader>
                  <CardTitle className="text-gray-900 flex items-center gap-2">
                    <User className="h-5 w-5" />
                    Personal Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-3">
                      <Label className="text-sm font-medium text-gray-700">
                        Username
                      </Label>
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <User className="h-4 w-4 text-gray-400" />
                        <span className="text-gray-900">{user?.username}</span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <Label className="text-sm font-medium text-gray-700">
                        Email
                      </Label>
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <Mail className="h-4 w-4 text-gray-400" />
                        <span className="text-gray-900">{user?.email}</span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <Label className="text-sm font-medium text-gray-700">
                        Role
                      </Label>
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <Shield className="h-4 w-4 text-gray-400" />
                        <span className="text-gray-900">{user?.role_name}</span>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <Label className="text-sm font-medium text-gray-700">
                        Account Created
                      </Label>
                      <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <Calendar className="h-4 w-4 text-gray-400" />
                        <span className="text-gray-900">
                          {user?.created_at
                            ? new Date(user.created_at).toLocaleDateString()
                            : ""}
                        </span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-none shadow-none">
                <CardHeader>
                  <CardTitle className="text-gray-900">Permissions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <p className="text-sm text-gray-600">
                        You have {user?.permissions?.length || 0} permissions
                        assigned
                      </p>
                    </div>
                    <Separator />
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {user?.permissions?.map((permission) => (
                        <div
                          key={permission}
                          className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                        >
                          <div className="h-2 w-2 rounded-full bg-primary-blue" />
                          <span className="text-sm text-gray-900">
                            {permission}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Security Tab */}
            <TabsContent value="security" className="space-y-6">
              <Card className="border-none shadow-none">
                <CardHeader>
                  <CardTitle className="text-gray-900 flex items-center gap-2">
                    <Key className="h-5 w-5" />
                    Change Password
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <form
                    onSubmit={handlePasswordChange}
                    className="space-y-6 max-w-md"
                  >
                    <div className="space-y-3">
                      <Label
                        htmlFor="oldPassword"
                        className="text-sm font-medium text-gray-700"
                      >
                        Current Password
                      </Label>
                      <Input
                        id="oldPassword"
                        type="password"
                        value={oldPassword}
                        onChange={(e) => setOldPassword(e.target.value)}
                        placeholder="Enter current password"
                        className="bg-gray-50 border-gray-200"
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-3">
                        <Label
                          htmlFor="newPassword"
                          className="text-sm font-medium text-gray-700"
                        >
                          New Password
                        </Label>
                        <Input
                          id="newPassword"
                          type="password"
                          value={newPassword}
                          onChange={(e) => setNewPassword(e.target.value)}
                          placeholder="Enter new password"
                          className="bg-gray-50 border-gray-200"
                        />
                      </div>

                      <div className="space-y-3">
                        <Label
                          htmlFor="confirmPassword"
                          className="text-sm font-medium text-gray-700"
                        >
                          Confirm Password
                        </Label>
                        <Input
                          id="confirmPassword"
                          type="password"
                          value={confirmPassword}
                          onChange={(e) => setConfirmPassword(e.target.value)}
                          placeholder="Confirm new password"
                          className="bg-gray-50 border-gray-200"
                        />
                      </div>
                    </div>

                    <div className="flex gap-3">
                      <Button
                        type="submit"
                        className="bg-primary-blue hover:bg-primary-dark"
                      >
                        Update Password
                      </Button>
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => {
                          setOldPassword("");
                          setNewPassword("");
                          setConfirmPassword("");
                        }}
                        className="border-gray-300"
                      >
                        Clear
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>

              <Card className="border-none shadow-none">
                <CardHeader>
                  <CardTitle className="text-gray-900">Sessions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-4">
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium text-gray-900">
                            Current Session
                          </p>
                          <div className="flex items-center gap-2 mt-1">
                            <div className="h-2 w-2 rounded-full bg-green-500"></div>
                            <p className="text-sm text-gray-600">Active now</p>
                          </div>
                        </div>
                        <Badge className="bg-green-50 text-green-700 border-green-200">
                          Current
                        </Badge>
                      </div>
                      <div className="mt-4 text-sm text-gray-600">
                        <p>Location: New York, USA</p>
                        <p className="mt-1">Device: Chrome on Windows</p>
                        <p className="mt-1">
                          Last Active:{" "}
                          {new Date().toLocaleString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                            month: "short",
                            day: "numeric",
                          })}
                        </p>
                      </div>
                    </div>

                  </div>

                  <div className="pt-4 border-t border-gray-200">
                    <Button
                      variant="outline"
                      onClick={handleLogoutAll}
                      className="w-full border-red-200 text-red-600 hover:bg-red-50 hover:text-red-700"
                    >
                      <LogOut className="mr-2 h-4 w-4" />
                      Logout from All Devices
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Activity Tab */}
            <TabsContent value="activity" className="space-y-6">
              <Card className="border-none shadow-none">
                <CardHeader>
                  <CardTitle className="text-gray-900">
                    Recent Activity
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                        <div className="h-2 w-2 mt-2 rounded-full bg-primary-blue"></div>
                        <div className="flex-1">
                          <p className="text-sm text-gray-900">
                            Password changed
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            Just now • Security
                          </p>
                        </div>
                      </div>

                      <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                        <div className="h-2 w-2 mt-2 rounded-full bg-green-500"></div>
                        <div className="flex-1">
                          <p className="text-sm text-gray-900">
                            Logged in from new device
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            2 hours ago • Security
                          </p>
                        </div>
                      </div>

                      <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                        <div className="h-2 w-2 mt-2 rounded-full bg-blue-500"></div>
                        <div className="flex-1">
                          <p className="text-sm text-gray-900">
                            Profile information updated
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            Yesterday • Profile
                          </p>
                        </div>
                      </div>

                      <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                        <div className="h-2 w-2 mt-2 rounded-full bg-purple-500"></div>
                        <div className="flex-1">
                          <p className="text-sm text-gray-900">
                            New permission granted
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            3 days ago • Permissions
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-none shadow-none">
                <CardHeader>
                  <CardTitle className="text-gray-900">
                    Account Statistics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-gradient-to-br from-blue-50 to-primary-blue/10 rounded-lg">
                      <p className="text-sm text-gray-600">Active Sessions</p>
                      <p className="text-2xl font-bold text-gray-900 mt-2">1</p>
                    </div>
                    <div className="p-4 bg-gradient-to-br from-green-50 to-green-500/10 rounded-lg">
                      <p className="text-sm text-gray-600">Days Active</p>
                      <p className="text-2xl font-bold text-gray-900 mt-2">
                        {user?.created_at
                          ? Math.floor(
                              (new Date().getTime() -
                                new Date(user.created_at).getTime()) /
                                (1000 * 60 * 60 * 24)
                            )
                          : "0"}
                      </p>
                    </div>
                    <div className="p-4 bg-gradient-to-br from-purple-50 to-purple-500/10 rounded-lg">
                      <p className="text-sm text-gray-600">Total Permissions</p>
                      <p className="text-2xl font-bold text-gray-900 mt-2">
                        {user?.permissions?.length || 0}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
