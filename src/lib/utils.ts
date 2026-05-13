import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatValue(val: number, decimals: number = 2): string {
  return val.toFixed(decimals);
}
