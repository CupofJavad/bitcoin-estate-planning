/**
 * API Client for Bitcoin Estate Planning Platform
 * Centralized API communication with error handling
 */

import { getSession } from 'next-auth/react'
import { errorLogger } from './error-logger'
import { fetchWithRetry } from './api-retry'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const BASE_URL = `${API_URL}/api/v1`

// Health check function
async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000),
    })
    return response.ok
  } catch {
    return false
  }
}

// Helper function to get auth headers
async function getAuthHeaders(): Promise<HeadersInit> {
  const session = await getSession()
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }
  
  if (session?.accessToken) {
    headers['Authorization'] = `Bearer ${session.accessToken}`
  }
  
  return headers
}

export interface EstatePlan {
  id: number
  user_id: number
  name: string
  description: string | null
  bitcoin_address: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface EstatePlanWithRelations extends EstatePlan {
  beneficiaries: Beneficiary[]
  timelock_policies: TimelockPolicy[]
}

export interface Beneficiary {
  id: number
  estate_plan_id: number
  name: string
  email: string | null
  bitcoin_address: string | null
  allocation_percentage: number
  created_at: string
  updated_at: string
}

export interface TimelockPolicy {
  id: number
  estate_plan_id: number
  name: string
  description: string | null
  timelock_blocks: number
  trigger_condition: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

// Estate Plans API
export const estatePlansApi = {
  list: async (): Promise<EstatePlan[]> => {
    try {
      // Check backend health first
      const isHealthy = await checkBackendHealth()
      if (!isHealthy) {
        const err = new Error('Backend server is not responding. Please ensure the backend API is running at ' + API_URL)
        errorLogger.logError(
          'Backend health check failed',
          err,
          { action: 'health_check', component: 'estatePlansApi' }
        )
        throw err
      }

      const headers = await getAuthHeaders()
      const res = await fetch(`${BASE_URL}/estate-plans`, { 
        method: 'GET',
        headers,
        signal: AbortSignal.timeout(10000),
      })
      if (!res.ok) {
        const errorText = await res.text()
        let error
        try {
          error = JSON.parse(errorText)
        } catch {
          error = { detail: `Failed to fetch estate plans: ${res.status} ${res.statusText}` }
        }
        const errorObj = new Error(error.detail || 'Failed to fetch estate plans')
        errorLogger.logError(
          'Failed to fetch estate plans',
          errorObj,
          { action: 'list_estate_plans', component: 'estatePlansApi' },
          { method: 'GET', url: `${BASE_URL}/estate-plans`, headers: Object.fromEntries(Object.entries(headers)) },
          { status: res.status, statusText: res.statusText, body: errorText }
        )
        throw errorObj
      }
      return res.json()
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        const err = new Error('Unable to connect to the server. Please ensure the backend API is running at ' + API_URL)
        errorLogger.logError(
          'Network error fetching estate plans',
          err,
          { action: 'list_estate_plans', component: 'estatePlansApi' },
          { method: 'GET', url: `${BASE_URL}/estate-plans` }
        )
        throw err
      }
      if (error instanceof DOMException && error.name === 'AbortError') {
        const err = new Error('Request timeout. The server is taking too long to respond.')
        errorLogger.logError(
          'Timeout error fetching estate plans',
          err,
          { action: 'list_estate_plans', component: 'estatePlansApi' }
        )
        throw err
      }
      throw error
    }
  },

  get: async (id: number): Promise<EstatePlanWithRelations> => {
    try {
      const headers = await getAuthHeaders()
      const res = await fetch(`${BASE_URL}/estate-plans/${id}`, { headers })
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: `Failed to fetch estate plan: ${res.status} ${res.statusText}` }))
        throw new Error(error.detail || 'Failed to fetch estate plan')
      }
      return res.json()
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Unable to connect to the server. Please ensure the backend API is running at ' + API_URL)
      }
      throw error
    }
  },

  create: async (data: Omit<EstatePlan, 'id' | 'created_at' | 'updated_at' | 'user_id'>): Promise<EstatePlan> => {
    try {
      // Check backend health first
      const isHealthy = await checkBackendHealth()
      if (!isHealthy) {
        throw new Error('Backend server is not responding. Please ensure the backend API is running at ' + API_URL)
      }

      const headers = await getAuthHeaders()
      const res = await fetch(`${BASE_URL}/estate-plans`, {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
        signal: AbortSignal.timeout(10000),
      })
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: 'Failed to create estate plan' }))
        const errorObj = new Error(error.detail || 'Failed to create estate plan')
        errorLogger.logError(
          'Failed to create estate plan',
          errorObj,
          { action: 'create_estate_plan', component: 'estatePlansApi' },
          { method: 'POST', url: `${BASE_URL}/estate-plans`, body: data }
        )
        throw errorObj
      }
      return res.json()
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Unable to connect to the server. Please ensure the backend API is running at ' + API_URL)
      }
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw new Error('Request timeout. The server is taking too long to respond.')
      }
      throw error
    }
  },

  update: async (id: number, data: Partial<EstatePlan>): Promise<EstatePlan> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/estate-plans/${id}`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to update estate plan' }))
      throw new Error(error.detail || 'Failed to update estate plan')
    }
    return res.json()
  },

  delete: async (id: number): Promise<void> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/estate-plans/${id}`, {
      method: 'DELETE',
      headers,
    })
    if (!res.ok) throw new Error('Failed to delete estate plan')
  },
}

// Beneficiaries API
export const beneficiariesApi = {
  list: async (estate_plan_id?: number): Promise<Beneficiary[]> => {
    const headers = await getAuthHeaders()
    const url = estate_plan_id
      ? `${BASE_URL}/beneficiaries?estate_plan_id=${estate_plan_id}`
      : `${BASE_URL}/beneficiaries`
    const res = await fetch(url, { headers })
    if (!res.ok) throw new Error('Failed to fetch beneficiaries')
    return res.json()
  },

  get: async (id: number): Promise<Beneficiary> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/beneficiaries/${id}`, { headers })
    if (!res.ok) throw new Error('Failed to fetch beneficiary')
    return res.json()
  },

  create: async (data: Omit<Beneficiary, 'id' | 'created_at' | 'updated_at'>): Promise<Beneficiary> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/beneficiaries`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to create beneficiary' }))
      throw new Error(error.detail || 'Failed to create beneficiary')
    }
    return res.json()
  },

  update: async (id: number, data: Partial<Beneficiary>): Promise<Beneficiary> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/beneficiaries/${id}`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to update beneficiary' }))
      throw new Error(error.detail || 'Failed to update beneficiary')
    }
    return res.json()
  },

  delete: async (id: number): Promise<void> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/beneficiaries/${id}`, {
      method: 'DELETE',
      headers,
    })
    if (!res.ok) throw new Error('Failed to delete beneficiary')
  },
}

// Timelock Policies API
export const timelockPoliciesApi = {
  list: async (estate_plan_id?: number): Promise<TimelockPolicy[]> => {
    const headers = await getAuthHeaders()
    const url = estate_plan_id
      ? `${BASE_URL}/timelock-policies?estate_plan_id=${estate_plan_id}`
      : `${BASE_URL}/timelock-policies`
    const res = await fetch(url, { headers })
    if (!res.ok) throw new Error('Failed to fetch timelock policies')
    return res.json()
  },

  get: async (id: number): Promise<TimelockPolicy> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/timelock-policies/${id}`, { headers })
    if (!res.ok) throw new Error('Failed to fetch timelock policy')
    return res.json()
  },

  create: async (data: Omit<TimelockPolicy, 'id' | 'created_at' | 'updated_at'>): Promise<TimelockPolicy> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/timelock-policies`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to create timelock policy' }))
      throw new Error(error.detail || 'Failed to create timelock policy')
    }
    return res.json()
  },

  update: async (id: number, data: Partial<TimelockPolicy>): Promise<TimelockPolicy> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/timelock-policies/${id}`, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to update timelock policy' }))
      throw new Error(error.detail || 'Failed to update timelock policy')
    }
    return res.json()
  },

  delete: async (id: number): Promise<void> => {
    const headers = await getAuthHeaders()
    const res = await fetch(`${BASE_URL}/timelock-policies/${id}`, {
      method: 'DELETE',
      headers,
    })
    if (!res.ok) throw new Error('Failed to delete timelock policy')
  },
}

// Bitcoin API
export interface BitcoinAddressValidation {
  valid: boolean
  format: string
  network: string
  errors: string[]
}

export interface BitcoinBalance {
  address: string
  balance_btc: number
  balance_sats: number
  confirmed: boolean
  cached: boolean
  error?: string
  provider?: string
  last_updated?: string
}

export const bitcoinApi = {
  validateAddress: async (address: string, network?: string): Promise<BitcoinAddressValidation> => {
    try {
      const headers = await getAuthHeaders()
      const res = await fetch(`${BASE_URL}/bitcoin/validate`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ address, network }),
      })
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: 'Failed to validate address' }))
        throw new Error(error.detail || 'Failed to validate address')
      }
      return res.json()
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Unable to connect to the server. Please ensure the backend API is running at ' + API_URL)
      }
      throw error
    }
  },

  getBalance: async (address: string, useCache: boolean = true): Promise<BitcoinBalance> => {
    try {
      const headers = await getAuthHeaders()
      const res = await fetch(`${BASE_URL}/bitcoin/balance/${encodeURIComponent(address)}?use_cache=${useCache}`, {
        headers,
      })
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: 'Failed to fetch balance' }))
        throw new Error(error.detail || 'Failed to fetch balance')
      }
      return res.json()
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Unable to connect to the server. Please ensure the backend API is running at ' + API_URL)
      }
      throw error
    }
  },
}

// Chatbot API
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  message: string
  conversation_history?: ChatMessage[]
}

export interface ChatResponse {
  response: string
  model?: string
  error?: string
  timestamp: string
}

export const chatbotApi = {
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    try {
      const headers = await getAuthHeaders()
      const res = await fetch(`${BASE_URL}/chatbot/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify(request),
        signal: AbortSignal.timeout(30000) // 30 second timeout for AI responses
      })
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: 'Failed to send message' }))
        const errorObj = new Error(error.detail || 'Failed to send message')
        errorLogger.logError(
          'Failed to send chatbot message',
          errorObj,
          { action: 'chatbot_chat', component: 'chatbotApi' },
          { method: 'POST', url: `${BASE_URL}/chatbot/chat`, body: request }
        )
        throw errorObj
      }
      return res.json()
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Unable to connect to the server. Please ensure the backend API is running at ' + API_URL)
      }
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw new Error('Request timeout. The AI service is taking too long to respond.')
      }
      throw error
    }
  },

  getSuggestions: async (): Promise<string[]> => {
    try {
      const headers = await getAuthHeaders()
      const res = await fetch(`${BASE_URL}/chatbot/suggestions`, {
        headers,
        signal: AbortSignal.timeout(5000) // 5 second timeout
      })
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: 'Failed to fetch suggestions' }))
        throw new Error(error.detail || 'Failed to fetch suggestions')
      }
      return res.json()
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Unable to connect to the server. Please ensure the backend API is running at ' + API_URL)
      }
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw new Error('Request timeout. The server is taking too long to respond.')
      }
      throw error
    }
  },
}

