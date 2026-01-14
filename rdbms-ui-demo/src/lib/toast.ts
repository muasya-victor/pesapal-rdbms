import { toast } from "sonner";

export function showError(error: unknown) {
  if (error instanceof Error) {
    if (error.name === "ApiError") {
      // Handle API errors gracefully
      const message = error.message;

      if (message.includes("403") || message.includes("Forbidden")) {
        toast.error("Access Denied", {
          description: "You do not have permission to perform this action.",
        });
      } else if (message.includes("401") || message.includes("Unauthorized")) {
        toast.error("Session Expired", {
          description: "Please login again.",
        });
      } else if (message.includes("Network")) {
        toast.error("Connection Error", {
          description:
            "Unable to connect to the server. Please check your connection.",
        });
      } else {
        toast.error("Error", {
          description: message,
        });
      }
    } else {
      toast.error("Error", {
        description: error.message,
      });
    }
  } else {
    toast.error("An unexpected error occurred");
  }
}

export function showSuccess(message: string) {
  toast.success("Success", {
    description: message,
  });
}
