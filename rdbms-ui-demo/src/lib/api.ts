const API_BASE_URL = "http://localhost:3500/api";

export interface ApiError {
  error: string;
}

export interface DashboardData {
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

export interface User {
  id: number;
  username: string;
  email: string;
  role_name: string;
  permissions: string[];
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  stock: number;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  user: User;
}

export interface ProductsResponse {
  products: Product[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        credentials: "include",
      });

      const data = await response.json();

      if (!response.ok) {
        const errorMessage =
          data.error || `Request failed with status ${response.status}`;
        const error = new Error(errorMessage);
        error.name = "ApiError"(error as any).status = response.status;
        throw error;
      }

      return this.parseNumbers(data);
    } catch (error) {
      if (error instanceof Error && error.name === "ApiError") {
        throw error;
      }

      const networkError = new Error(
        error instanceof Error ? error.message : "Network error"
      );
      networkError.name = "NetworkError";
      throw networkError;
    }
  }

  private parseNumbers<T>(data: any): T {
    if (Array.isArray(data)) {
      return data.map((item) => this.parseNumbers(item)) as T;
    }

    if (data !== null && typeof data === "object") {
      const parsed: any = {};
      for (const key in data) {
        const value = data[key];

        if (
          key === "price" ||
          key === "stock" ||
          key === "id" ||
          key === "created_by"
        ) {
          if (value === null || value === undefined) {
            parsed[key] = 0;
          } else if (typeof value === "string") {
            const num = parseFloat(value);
            parsed[key] = isNaN(num) ? 0 : num;
          } else {
            parsed[key] = Number(value) || 0;
          }
        } else if (key === "products" && Array.isArray(value)) {
          parsed[key] = value.map((product) => this.parseNumbers(product));
        } else if (key === "product" && value && typeof value === "object") {
          parsed[key] = this.parseNumbers(value);
        } else {
          parsed[key] = this.parseNumbers(value);
        }
      }
      return parsed;
    }

    return data;
  }

  async login(data: LoginRequest): Promise<LoginResponse> {
    return this.request("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getDashboardData(): Promise<DashboardData> {
    return this.request("/analytics/dashboard");
  }

  async register(
    username: string,
    email: string,
    password: string,
    role: string = "user"
  ) {
    return this.request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password, role }),
    });
  }

  async logout() {
    return this.request("/auth/logout", { method: "POST" });
  }

  async getProfile(): Promise<{ user: User }> {
    try {
      return await this.request("/auth/profile");
    } catch (error) {
      if (error instanceof Error && error.name === "ApiError") {
        const apiError = error as any;
        if (apiError.status === 401) {
          return { user: null } as any;
        }
      }
      throw error;
    }
  }

  async getPermissions(): Promise<{ permissions: string[] }> {
    return this.request("/auth/permissions");
  }

  async getProducts(
    page: number = 1,
    perPage: number = 10
  ): Promise<ProductsResponse> {
    return this.request(`/products?page=${page}&per_page=${perPage}`);
  }

  async getProduct(id: number): Promise<{ product: Product }> {
    return this.request(`/products/${id}`);
  }

  async createProduct(
    productData: Omit<
      Product,
      "id" | "created_by" | "created_at" | "updated_at"
    >
  ) {
    const product = {
      ...productData,
      price:
        typeof productData.price === "string"
          ? parseFloat(productData.price)
          : productData.price,
      stock:
        typeof productData.stock === "string"
          ? parseInt(productData.stock)
          : productData.stock,
    };

    return this.request("/products", {
      method: "POST",
      body: JSON.stringify(product),
    });
  }

  async updateProduct(id: number, updates: Partial<Product>) {
    const parsedUpdates: any = { ...updates };
    if ("price" in updates) {
      parsedUpdates.price =
        typeof updates.price === "string"
          ? parseFloat(updates.price)
          : updates.price;
    }
    if ("stock" in updates) {
      parsedUpdates.stock =
        typeof updates.stock === "string"
          ? parseInt(updates.stock)
          : updates.stock;
    }

    return this.request(`/products/${id}`, {
      method: "PUT",
      body: JSON.stringify(parsedUpdates),
    });
  }

  async deleteProduct(id: number) {
    return this.request(`/products/${id}`, { method: "DELETE" });
  }

  async searchProducts(query: string, category?: string) {
    const params = new URLSearchParams({ q: query });
    if (category) params.append("category", category);
    return this.request(`/products/search?${params.toString()}`);
  }

  async getUsers(): Promise<{ users: User[] }> {
    try {
      return await this.request("/users");
    } catch (error) {
      if (error instanceof Error && error.name === "ApiError") {
        const apiError = error as any;
        if (apiError.status === 403) {
          return { users: [] };
        }
      }
      throw error;
    }
  }

  async updateUserRole(userId: number, role: string) {
    return this.request(`/users/${userId}/role`, {
      method: "PUT",
      body: JSON.stringify({ role }),
    });
  }
}

export const api = new ApiClient();
