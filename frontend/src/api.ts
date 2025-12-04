/**
 * API service for communicating with the FastAPI backend
 */

import type { Element, Stats, CombineResponse } from './types';

const API_BASE_URL = 'http://localhost:8000';

export const api = {
  /**
   * Get all discovered elements
   */
  async getElements(): Promise<Element[]> {
    const response = await fetch(`${API_BASE_URL}/elements`);
    if (!response.ok) throw new Error('Failed to fetch elements');
    return response.json();
  },

  /**
   * Combine two elements
   */
  async combineElements(element1Id: number, element2Id: number): Promise<CombineResponse> {
    const response = await fetch(`${API_BASE_URL}/combine`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        element1_id: element1Id,
        element2_id: element2Id,
      }),
    });
    if (!response.ok) throw new Error('Failed to combine elements');
    return response.json();
  },

  /**
   * Get game statistics
   */
  async getStats(): Promise<Stats> {
    const response = await fetch(`${API_BASE_URL}/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },
};
