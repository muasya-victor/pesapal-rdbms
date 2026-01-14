// src/components/Unauthorized.tsx
import { ShieldAlert, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useRouter } from "next/navigation";

interface UnauthorizedProps {
  title?: string;
  message?: string;
  showBackButton?: boolean;
}

export default function Unauthorized({
  title = "Access Denied",
  message = "You don't have permission to view this page.",
  showBackButton = true,
}: UnauthorizedProps) {
  const router = useRouter();

  return (
    <div className="min-h-[60vh] flex items-center justify-center p-4">
      <Card className="w-full max-w-md border-2 border-primary-red">
        <CardHeader className="text-center">
          <div className="mx-auto w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mb-4">
            <ShieldAlert className="h-8 w-8 text-primary-red" />
          </div>
          <CardTitle className="text-2xl text-primary-red">{title}</CardTitle>
        </CardHeader>

        <CardContent className="text-center space-y-6">
          <div className="space-y-2">
            <p className="text-gray-600">{message}</p>
            <p className="text-sm text-gray-500">
              Please contact an administrator if you believe this is an error.
            </p>
          </div>

          {showBackButton && (
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Button
                onClick={() => router.back()}
                variant="outline"
                className="border-primary-blue text-primary-blue hover:bg-primary-blue hover:text-white"
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Go Back
              </Button>

              <Button
                onClick={() => router.push("/dashboard")}
                className="bg-primary-blue hover:bg-primary-dark"
              >
                Go to Dashboard
              </Button>
            </div>
          )}

          <div className="pt-4 border-t">
            <p className="text-xs text-gray-500">Error code: 403 - Forbidden</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
