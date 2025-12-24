'use client'

import { useEffect, useState } from 'react'

interface EstatePlan {
  id: number
  name: string
  description: string | null
  bitcoin_address: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export default function Home() {
  const [estatePlans, setEstatePlans] = useState<EstatePlan[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchEstatePlans = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/v1/estate-plans`)
        if (!response.ok) {
          throw new Error('Failed to fetch estate plans')
        }
        const data = await response.json()
        setEstatePlans(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred')
      } finally {
        setLoading(false)
      }
    }

    fetchEstatePlans()
  }, [])

  if (loading) {
    return (
      <main style={{ padding: '2rem', textAlign: 'center' }}>
        <h1>Bitcoin Estate Planning Platform</h1>
        <p>Loading...</p>
      </main>
    )
  }

  if (error) {
    return (
      <main style={{ padding: '2rem', textAlign: 'center' }}>
        <h1>Bitcoin Estate Planning Platform</h1>
        <p style={{ color: 'red' }}>Error: {error}</p>
        <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
          Make sure the backend API is running at {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
        </p>
      </main>
    )
  }

  return (
    <main style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem' }}>Bitcoin Estate Planning Platform</h1>
      
      <div style={{ marginBottom: '2rem' }}>
        <h2>Estate Plans</h2>
        {estatePlans.length === 0 ? (
          <p style={{ color: '#666', marginTop: '1rem' }}>No estate plans found. Create one via the API.</p>
        ) : (
          <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
            {estatePlans.map((plan) => (
              <div
                key={plan.id}
                style={{
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  padding: '1.5rem',
                  backgroundColor: '#f9f9f9',
                }}
              >
                <h3 style={{ marginBottom: '0.5rem' }}>{plan.name}</h3>
                {plan.description && (
                  <p style={{ color: '#666', marginBottom: '0.5rem' }}>{plan.description}</p>
                )}
                {plan.bitcoin_address && (
                  <p style={{ fontFamily: 'monospace', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
                    Address: {plan.bitcoin_address}
                  </p>
                )}
                <p style={{ fontSize: '0.9rem', color: plan.is_active ? 'green' : 'gray' }}>
                  Status: {plan.is_active ? 'Active' : 'Inactive'}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}

