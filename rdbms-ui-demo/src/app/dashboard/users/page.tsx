"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Users,
  ChevronLeft,
  ChevronRight,
  Shield,
  ShieldCheck,
  ShieldOff,
} from "lucide-react";
import { api, User } from "@/lib/api";
import { toast } from "sonner";
import { useAuth } from "@/contexts/AuthContext";
import Unauthorized from "@/components/Unauthorized";
import { Skeleton } from "@/components/ui/skeleton";

export default function UsersPage() {
  const { user, hasPermission } = useAuth();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [accessDenied, setAccessDenied] = useState(false);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const [perPage, setPerPage] = useState(10);
  const [search, setSearch] = useState("");

  useEffect(() => {
    if (hasPermission("view_users") || hasPermission("manage_roles")) {
      fetchUsers();
    } else {
      setAccessDenied(true);
      setLoading(false);
    }
  }, [hasPermission, currentPage, perPage]);

  const fetchUsers = async () => {
    try {
      // Note: Your API doesn't support pagination for users yet
      // This is a client-side pagination implementation
      const { users } = await api.getUsers();
      setUsers(users);
      setTotalUsers(users.length);
      setTotalPages(Math.ceil(users.length / perPage));
    } catch (error) {
      if (
        (error instanceof Error && error.message.includes("403")) ||
        error.message.includes("Forbidden")
      ) {
        setAccessDenied(true);
      } else {
        toast.error("Failed to fetch users");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = async (userId: number, newRole: string) => {
    try {
      await api.updateUserRole(userId, newRole);
      toast.success("Role updated successfully");
      fetchUsers();
    } catch (error) {
      if (error instanceof Error && error.message.includes("403")) {
        toast.error("You do not have permission to update roles");
      } else {
        toast.error("Failed to update role");
      }
    }
  };

  const filteredUsers = users.filter(
    (user) =>
      user.username.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase()) ||
      user.role_name.toLowerCase().includes(search.toLowerCase())
  );

  // Client-side pagination
  const paginatedUsers = filteredUsers.slice(
    (currentPage - 1) * perPage,
    currentPage * perPage
  );

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const handlePerPageChange = (value: string) => {
    const newPerPage = parseInt(value);
    setPerPage(newPerPage);
    setCurrentPage(1);
  };

  if (accessDenied) {
    return <Unauthorized />;
  }

  const getRoleBadge = (role: string) => {
    const colors: Record<string, string> = {
      admin: "bg-red-50 text-red-700 border-red-200",
      manager: "bg-blue-50 text-primary-blue border-blue-200",
      user: "bg-gray-50 text-gray-700 border-gray-200",
      viewer: "bg-gray-100 text-gray-700 border-gray-300",
    };

    return (
      <Badge variant="outline" className={colors[role] || "bg-gray-50"}>
        {role.charAt(0).toUpperCase() + role.slice(1)}
      </Badge>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Users</h1>
          <p className="text-gray-600 mt-2">
            Manage user accounts and permissions
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Users className="h-5 w-5 text-primary-blue" />
          <span className="font-semibold">{users.length} users</span>
        </div>
      </div>

      <Card className="border-none shadow-none  ">
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <CardTitle className="text-gray-900">User Management</CardTitle>
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                placeholder="Search users..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded text-sm w-full sm:w-64"
              />
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600 whitespace-nowrap">
                  Show:
                </span>
                <select
                  value={perPage}
                  onChange={(e) => handlePerPageChange(e.target.value)}
                  className="px-2 py-1 border border-gray-300 rounded text-sm"
                >
                  <option value="5">5</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                </select>
                <span className="text-sm text-gray-600 whitespace-nowrap">
                  per page
                </span>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          {loading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : (
            <>
              <div className="rounded-md border-0">
                <Table>
                  <TableHeader>
                    <TableRow className="border-b border-gray-200">
                      <TableHead className="font-semibold text-gray-900">
                        User
                      </TableHead>
                      <TableHead className="font-semibold text-gray-900">
                        Email
                      </TableHead>
                      <TableHead className="font-semibold text-gray-900">
                        Role
                      </TableHead>
                      <TableHead className="font-semibold text-gray-900">
                        Joined
                      </TableHead>
                      <TableHead className="font-semibold text-gray-900">
                        Permissions
                      </TableHead>
                      <TableHead className="font-semibold text-gray-900 text-right">
                        Actions
                      </TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {paginatedUsers.length > 0 ? (
                      paginatedUsers.map((user) => (
                        <TableRow
                          key={user.id}
                          className="border-b border-gray-100 hover:bg-gray-50"
                        >
                          <TableCell className="py-4">
                            <div className="font-medium text-gray-900">
                              {user.username}
                            </div>
                          </TableCell>
                          <TableCell className="text-gray-600">
                            {user.email}
                          </TableCell>
                          <TableCell>{getRoleBadge(user.role_name)}</TableCell>
                          <TableCell>
                            {new Date(user.created_at).toLocaleDateString()}
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {user.permissions?.slice(0, 3).map((perm) => (
                                <Badge
                                  key={perm}
                                  variant="outline"
                                  className="text-xs bg-gray-50 border-gray-200"
                                >
                                  {perm}
                                </Badge>
                              ))}
                              {user.permissions?.length > 3 && (
                                <Badge
                                  variant="outline"
                                  className="text-xs bg-gray-50 border-gray-200"
                                >
                                  +{user.permissions.length - 3} more
                                </Badge>
                              )}
                            </div>
                          </TableCell>
                          <TableCell className="text-right">
                            <div className="flex justify-end gap-2">
                              {hasPermission("manage_roles") && (
                                <Select
                                  value={user.role_name}
                                  onValueChange={(value) =>
                                    handleRoleChange(user.id, value)
                                  }
                                >
                                  <SelectTrigger className="w-32 border-gray-300">
                                    <SelectValue placeholder="Change role" />
                                  </SelectTrigger>
                                  <SelectContent>
                                    <SelectItem value="admin">Admin</SelectItem>
                                    <SelectItem value="manager">
                                      Manager
                                    </SelectItem>
                                    <SelectItem value="user">User</SelectItem>
                                    <SelectItem value="viewer">
                                      Viewer
                                    </SelectItem>
                                  </SelectContent>
                                </Select>
                              )}
                            </div>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell
                          colSpan={6}
                          className="text-center py-8 text-gray-500"
                        >
                          No users found
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </div>

              {/* Pagination Controls */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between border-t border-gray-200 pt-4 mt-4">
                  <div className="text-sm text-gray-700">
                    Showing{" "}
                    <span className="font-medium">
                      {(currentPage - 1) * perPage + 1}
                    </span>{" "}
                    to{" "}
                    <span className="font-medium">
                      {Math.min(currentPage * perPage, totalUsers)}
                    </span>{" "}
                    of <span className="font-medium">{totalUsers}</span> users
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="border-gray-300"
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </Button>

                    <div className="flex items-center space-x-1">
                      {Array.from(
                        { length: Math.min(5, totalPages) },
                        (_, i) => {
                          let pageNum;
                          if (totalPages <= 5) {
                            pageNum = i + 1;
                          } else if (currentPage <= 3) {
                            pageNum = i + 1;
                          } else if (currentPage >= totalPages - 2) {
                            pageNum = totalPages - 4 + i;
                          } else {
                            pageNum = currentPage - 2 + i;
                          }

                          return (
                            <Button
                              key={pageNum}
                              variant={
                                currentPage === pageNum ? "default" : "outline"
                              }
                              size="sm"
                              onClick={() => handlePageChange(pageNum)}
                              className={
                                currentPage === pageNum
                                  ? "bg-primary-blue text-white"
                                  : "border-gray-300"
                              }
                            >
                              {pageNum}
                            </Button>
                          );
                        }
                      )}
                    </div>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === totalPages}
                      className="border-gray-300"
                    >
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
