import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function toNumber(value: any): number {
  if (value === null || value === undefined) return 0;
  if (typeof value === "number") return value;
  if (typeof value === "string") {
    const parsed = parseFloat(value);
    return isNaN(parsed) ? 0 : parsed;
  }
  return Number(value) || 0;
}

export function formatPrice(price: any): string {
  const num = toNumber(price);
  return `KES ${num.toFixed(2)}`;
}

export function formatStock(stock: any): number {
  return toNumber(stock);
}

export function safeToFixed(value: any, decimals: number = 2): string {
  const num = toNumber(value);
  return num.toFixed(decimals);
}
