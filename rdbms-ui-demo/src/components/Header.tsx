// src/components/Header.tsx
"use client";

import { ChevronDown, UserCircle, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import Link from "next/link";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 flex h-16 items-center justify-between bg-linear-to-r from-white to-gray-50 px-6">
      {/* Left side - Brand/App Name */}
      <div className="flex items-center gap-3">
        <div className="h-8 w-1 bg-linear-to-b from-primary-blue to-primary-dark rounded-full" />
        <div>
          <h1 className="text-lg font-semibold text-gray-900">
            RDBMS Dashboard
          </h1>
          <p className="text-xs text-gray-500">Database Management Demo</p>
        </div>
      </div>

      {/* Right side - User Profile */}
      <div className="flex items-center gap-4">


        <div className="h-6 w-px bg-linear-to-b from-transparent via-gray-200 to-transparent" />

        {/* User Profile Dropdown */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className="group flex items-center gap-3 px-3 py-2 hover:bg-primary-blue/5 rounded-xl transition-all"
            >
              <div className="relative">
                <div className="h-9 w-9 rounded-full bg-linear-to-br from-primary-blue to-primary-dark flex items-center justify-center">
                  <UserCircle className="h-6 w-6 text-white" />
                </div>
                <div className="absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full border-2 border-white bg-emerald-500" />
              </div>

              <div className="hidden md:block text-left">
                <div className="flex items-center gap-2">
                  <p className="text-sm font-semibold text-gray-900">
                    {user?.username}
                  </p>
                  <span className="px-2 py-0.5 text-xs font-medium bg-primary-blue/10 text-primary-blue rounded-full">
                    {user?.role_name}
                  </span>
                </div>
                <p className="text-xs text-gray-500 truncate max-w-[160px]">
                  {user?.email}
                </p>
              </div>

              <ChevronDown className="h-4 w-4 text-gray-400 group-hover:text-primary-blue transition-colors" />
            </Button>
          </DropdownMenuTrigger>

          <DropdownMenuContent
            align="end"
            className="w-64 border-none shadow-xl rounded-xl"
          >
            <DropdownMenuLabel className="flex items-center gap-3 p-4">
              <div className="h-10 w-10 rounded-full bg-linear-to-br from-primary-blue to-primary-dark flex items-center justify-center">
                <UserCircle className="h-6 w-6 text-white" />
              </div>
              <div>
                <p className="font-semibold text-gray-900">{user?.username}</p>
                <p className="text-sm text-gray-500">{user?.email}</p>
                <span className="inline-block mt-1 px-2 py-0.5 text-xs font-medium bg-primary-blue/10 text-primary-blue rounded-full">
                  {user?.role_name}
                </span>
              </div>
            </DropdownMenuLabel>

            <DropdownMenuSeparator className="bg-gray-100" />

            <div className="px-2 py-1.5">
              <div className="text-xs text-gray-500 px-3 py-1.5">
                Account ID: {user?.id}
              </div>
              <div className="text-xs text-gray-500 px-3 py-1.5">
                Joined:{" "}
                {user?.created_at
                  ? new Date(user.created_at).toLocaleDateString()
                  : "N/A"}
              </div>
            </div>

            <DropdownMenuSeparator className="bg-gray-100" />

            <DropdownMenuItem className="flex items-center gap-3 px-3 py-2.5 cursor-pointer hover:bg-gray-50 rounded-lg">
              <Link href="/dashboard/profile" className="flex items-center gap-3">
                <UserCircle className="h-4 w-4 text-gray-500" />
                <span className="text-sm text-gray-700">Profile</span>
              </Link>
            </DropdownMenuItem>

            <DropdownMenuSeparator className="bg-gray-100" />

            <DropdownMenuItem
              onClick={logout}
              className="flex items-center gap-3 px-3 py-2.5 cursor-pointer hover:bg-red-50 text-red-600 hover:text-red-700 rounded-lg"
            >
              <div className="h-4 w-4 rounded-full border border-red-300 flex items-center justify-center">
                <div className="h-1.5 w-1.5 rounded-full bg-red-500" />
              </div>
              <span className="text-sm font-medium">Sign Out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
