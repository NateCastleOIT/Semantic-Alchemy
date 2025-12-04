/**
 * Type definitions for the Semantic Alchemy application
 */

export interface Element {
  id: number;
  name: string;
  emoji: string;
  definition: string;
  is_base: boolean;
  tags: string[];
  behavior_hints: string[];
  parent_a_id?: string;
  parent_b_id?: string;
  parent_a_name?: string;
  parent_b_name?: string;
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
