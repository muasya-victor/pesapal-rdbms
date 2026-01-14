// Update src/app/(dashboard)/page.tsx
"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Package,
  Users,
  DollarSign,
  TrendingUp,
  ShoppingCart,
  Clock,
  BarChart3,
  Activity,
  TrendingDown,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Skeleton } from "@/components/ui/skeleton";
import { formatPrice } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface DashboardData {
  summary: {
    total_products: number;
    total_users: number;
    total_value: number;
    total_revenue: number;
    growth_rate: number;
    low_stock_count: number;
    average_price: number;
  };
  recent: {
    products: Array<{
      id: number;
      name: string;
      description: string;
      price: number;
      category: string;
      stock: number;
      created_at: string;
      status: string;
    }>;
    users: Array<{
      id: number;
      username: string;
      email: string;
      role_name: string;
      created_at: string;
    }>;
  };
  insights: {
    top_categories: [string, number][];
    stock_status: {
      low_stock: number;
      in_stock: number;
    };
  };
  activity: Array<{
    type: string;
    message: string;
    time: string;
    icon: string;
    color: string;
  }>;
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // We'll add this method to your api.ts
      const dashboardData = await api.getDashboardData();
      setData(dashboardData);
    } catch (err) {
      setError("Failed to load dashboard data");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Add to your api.ts file
  // async getDashboardData(): Promise<DashboardData> {
  //   return this.request("/analytics/dashboard");
  // }

  const statCards = [
    {
      name: "Total Products",
      value: data?.summary.total_products ?? 0,
      icon: Package,
      color: "text-blue-600",
      bgColor: "bg-gradient-to-br from-blue-50 to-blue-100",
      description: "Active in inventory",
    },
    {
      name: "Total Users",
      value: data?.summary.total_users ?? 0,
      icon: Users,
      color: "text-green-600",
      bgColor: "bg-gradient-to-br from-green-50 to-green-100",
      description: "Registered accounts",
    },
    {
      name: "Inventory Value",
      value: formatPrice(data?.summary.total_value ?? 0),
      icon: DollarSign,
      color: "text-purple-600",
      bgColor: "bg-gradient-to-br from-purple-50 to-purple-100",
      description: "Total stock worth",
    },
    {
      name: "Monthly Growth",
      value:
        data?.summary.growth_rate !== undefined
          ? `${data.summary.growth_rate.toFixed(1)}%`
          : "0%",
      icon: data?.summary.growth_rate >= 0 ? TrendingUp : TrendingDown,
      color:
        data?.summary.growth_rate >= 0 ? "text-emerald-600" : "text-red-600",
      bgColor:
        data?.summary.growth_rate >= 0
          ? "bg-gradient-to-br from-emerald-50 to-emerald-100"
          : "bg-gradient-to-br from-red-50 to-red-100",
      description: "Product growth rate",
    },
  ];

  const insightCards = [
    {
      title: "Low Stock Alert",
      value: data?.summary.low_stock_count ?? 0,
      icon: ShoppingCart,
      color: "text-orange-600",
      bgColor: "bg-gradient-to-br from-orange-50 to-orange-100",
      description: "Items below 10 units",
      action: "Restock needed",
    },
    {
      title: "Average Price",
      value: formatPrice(data?.summary.average_price ?? 0),
      icon: BarChart3,
      color: "text-indigo-600",
      bgColor: "bg-gradient-to-br from-indigo-50 to-indigo-100",
      description: "Per product",
      action: "Market analysis",
    },
    {
      title: "Recent Updates",
      value:
        (data?.recent.products.length || 0) + (data?.recent.users.length || 0),
      icon: Clock,
      color: "text-cyan-600",
      bgColor: "bg-gradient-to-br from-cyan-50 to-cyan-100",
      description: "Last 30 days",
      action: "View activity",
    },
  ];

  const getIconComponent = (iconName: string) => {
    const icons: Record<string, React.ReactNode> = {
      Package: <Package className="h-4 w-4" />,
      User: <Users className="h-4 w-4" />,
      Activity: <Activity className="h-4 w-4" />,
    };
    return icons[iconName] || <Activity className="h-4 w-4" />;
  };

  const getColorClass = (color: string) => {
    const colors: Record<string, string> = {
      blue: "bg-blue-50 text-blue-600",
      green: "bg-green-50 text-green-600",
      purple: "bg-purple-50 text-purple-600",
      orange: "bg-orange-50 text-orange-600",
    };
    return colors[color] || "bg-gray-50 text-gray-600";
  };

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary-blue/5 to-primary-dark/5 rounded-2xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Welcome back,{" "}
              <span className="text-primary-blue">{user?.username}</span>!
            </h1>
            <p className="text-gray-600 mt-2">
              Here's what's happening with your business today.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className="px-4 py-2 bg-white rounded-lg border border-gray-200">
              <p className="text-sm text-gray-600">Local time</p>
              <p className="font-medium text-gray-900">
                {new Date().toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </p>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Key Metrics */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Key Metrics
        </h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {statCards.map((stat, idx) => (
            <Card
              key={idx}
              className="border-none shadow-none overflow-hidden bg-white"
            >
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 mb-1">
                      {stat.name}
                    </p>
                    {loading ? (
                      <Skeleton className="h-9 w-24 mt-2" />
                    ) : (
                      <>
                        <p className="text-2xl font-bold text-gray-900">
                          {stat.value}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {stat.description}
                        </p>
                      </>
                    )}
                  </div>
                  <div className={`rounded-xl p-3 ${stat.bgColor}`}>
                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
                {stat.name === "Monthly Growth" && data && !loading && (
                  <div className="mt-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Performance</span>
                      <Badge
                        className={
                          data.summary.growth_rate >= 0
                            ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                            : "bg-red-50 text-red-700 border-red-200"
                        }
                      >
                        {data.summary.growth_rate >= 0
                          ? "↑ Positive"
                          : "↓ Negative"}
                      </Badge>
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden mt-2">
                      <div
                        className={`h-full rounded-full ${
                          data.summary.growth_rate >= 0
                            ? "bg-emerald-500"
                            : "bg-red-500"
                        }`}
                        style={{
                          width: `${Math.min(
                            Math.abs(data.summary.growth_rate),
                            100
                          )}%`,
                        }}
                      />
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Business Insights */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Business Insights
        </h2>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {insightCards.map((insight, idx) => (
            <Card key={idx} className="border-none shadow-none bg-white">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className={`rounded-lg p-2 ${insight.bgColor}`}>
                    <insight.icon className={`h-5 w-5 ${insight.color}`} />
                  </div>
                  <Badge variant="outline" className="text-xs font-normal">
                    {insight.action}
                  </Badge>
                </div>
                <div>
                  {loading ? (
                    <Skeleton className="h-7 w-20 mb-2" />
                  ) : (
                    <p className="text-2xl font-bold text-gray-900">
                      {insight.value}
                    </p>
                  )}
                  <p className="text-sm font-medium text-gray-900">
                    {insight.title}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {insight.description}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent Activity Section */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Products */}
        <Card className="border-none shadow-none bg-white">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-gray-900">
              <Package className="h-5 w-5 text-primary-blue" />
              Recent Products
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="space-y-4">
                {[...Array(3)].map((_, i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            ) : data?.recent.products && data.recent.products.length > 0 ? (
              <div className="space-y-4">
                {data.recent.products.map((product) => (
                  <div
                    key={product.id}
                    className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <div className="bg-blue-50 p-2 rounded-lg">
                        <Package className="h-4 w-4 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">
                          {product.name}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <Badge
                            variant="outline"
                            className="text-xs font-normal border-blue-200 text-blue-700 bg-blue-50"
                          >
                            {product.category}
                          </Badge>
                          <span className="text-xs text-gray-500">
                            Added{" "}
                            {new Date(product.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">
                        {formatPrice(product.price)}
                      </p>
                      <p
                        className={`text-xs ${
                          product.stock < 10 ? "text-red-600" : "text-gray-500"
                        }`}
                      >
                        {product.stock} in stock
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="bg-gray-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Package className="h-8 w-8 text-gray-400" />
                </div>
                <p className="text-gray-900 font-medium">No products yet</p>
                <p className="text-gray-500 text-sm mt-1">
                  Start adding products to see them here
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Activity Stream */}
        <Card className="border-none shadow-none bg-white">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-gray-900">
              <Activity className="h-5 w-5 text-primary-blue" />
              Activity Stream
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {loading ? (
                [...Array(3)].map((_, i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))
              ) : data?.activity && data.activity.length > 0 ? (
                <>
                  {data.activity.map((activity, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors"
                    >
                      <div
                        className={`rounded-lg p-2 ${getColorClass(
                          activity.color
                        )}`}
                      >
                        {getIconComponent(activity.icon)}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-900">
                          {activity.message}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </>
              ) : (
                <div className="text-center py-8">
                  <div className="bg-gray-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Activity className="h-8 w-8 text-gray-400" />
                  </div>
                  <p className="text-gray-900 font-medium">
                    No recent activity
                  </p>
                  <p className="text-gray-500 text-sm mt-1">
                    Activity will appear here
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Summary Card */}
      {data && !loading && (
        <Card className="border-none shadow-none bg-gradient-to-r from-primary-blue/5 to-primary-dark/5">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Today's Summary
                </h3>
                <p className="text-gray-600 mt-1">
                  Your inventory is worth{" "}
                  {formatPrice(data.summary.total_value)} across{" "}
                  {data.summary.total_products} products
                  {data.summary.low_stock_count > 0 && (
                    <span className="text-orange-600 font-medium">
                      {" "}
                      • {data.summary.low_stock_count} need restocking
                    </span>
                  )}
                </p>
              </div>
              <Button
                variant="outline"
                className="border-primary-blue text-primary-blue hover:bg-primary-blue hover:text-white"
                onClick={fetchDashboardData}
                disabled={loading}
              >
                {loading ? "Refreshing..." : "Refresh Data"}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
