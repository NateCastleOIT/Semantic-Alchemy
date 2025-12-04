/**
 * Type definitions for the Semantic Alchemy application
 */

export interface Element {
  id: number;
  name: string;
  emoji: string;
  definition: string;
}

export interface Stats {
  total_elements: number;
  base_elements: number;
  discovered_elements: number;
}

export interface CombineResponse {
  success: boolean;
  result?: Element;
  was_discovered?: boolean;
  message?: string;
}
