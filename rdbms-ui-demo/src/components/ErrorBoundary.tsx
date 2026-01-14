"use client";

import { Component, ErrorInfo, ReactNode } from "react";
import { AlertTriangle, RefreshCw, Bug } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      const error = this.state.error;
      const isPriceError =
        error?.message?.includes("price") ||
        error?.message?.includes("toFixed") ||
        error?.message?.includes("is not a function");

      if (isPriceError) {
        return (
          <div className="min-h-[60vh] flex items-center justify-center p-4">
            <Card className="w-full max-w-md border-2 border-primary-red">
              <CardHeader className="text-center">
                <div className="mx-auto w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mb-4">
                  <Bug className="h-8 w-8 text-primary-red" />
                </div>
                <CardTitle className="text-2xl text-primary-red">
                  Data Format Issue
                </CardTitle>
              </CardHeader>

              <CardContent className="text-center space-y-6">
                <div className="space-y-2">
                  <p className="text-gray-600">
                    There's an issue with data formatting. This is usually
                    temporary.
                  </p>
                  <p className="text-sm text-gray-500">
                    The app will automatically fix this when you refresh.
                  </p>
                </div>

                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <Button
                    onClick={() => window.location.reload()}
                    className="bg-primary-blue hover:bg-primary-dark"
                  >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Refresh Page
                  </Button>
                </div>

                <div className="pt-4 border-t">
                  <p className="text-xs text-gray-500">
                    Error: {error?.message}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        );
      }

      return (
        <div className="min-h-[60vh] flex items-center justify-center p-4">
          <Card className="w-full max-w-md border-2 border-primary-red">
            <CardHeader className="text-center">
              <div className="mx-auto w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mb-4">
                <AlertTriangle className="h-8 w-8 text-primary-red" />
              </div>
              <CardTitle className="text-2xl text-primary-red">
                Something went wrong
              </CardTitle>
            </CardHeader>

            <CardContent className="text-center space-y-6">
              <div className="space-y-2">
                <p className="text-gray-600">
                  {error?.message || "An unexpected error occurred"}
                </p>
                <p className="text-sm text-gray-500">
                  Please try refreshing the page or contact support if the
                  problem persists.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Button
                  onClick={this.resetError}
                  className="bg-primary-blue hover:bg-primary-dark"
                >
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Try Again
                </Button>

                <Button
                  onClick={() => window.location.reload()}
                  variant="outline"
                  className="border-primary-blue text-primary-blue hover:bg-primary-blue hover:text-white"
                >
                  Refresh Page
                </Button>
              </div>

              <div className="pt-4 border-t">
                <p className="text-xs text-gray-500">
                  If this continues, please report the issue.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}
