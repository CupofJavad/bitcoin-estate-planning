'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { toast } from '@/components/ui/toast'
import { Eye, EyeOff } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Debug logging
if (typeof window !== 'undefined') {
  console.log('API URL:', API_URL)
}

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch(`${API_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          full_name: formData.full_name || undefined,
        }),
      })

      if (!response.ok) {
        let errorMessage = 'Registration failed'
        try {
          const error = await response.json()
          // Handle FastAPI Users error format
          if (error.detail) {
            if (typeof error.detail === 'string') {
              errorMessage = error.detail
            } else if (error.detail.code) {
              errorMessage = error.detail.code
            } else {
              errorMessage = JSON.stringify(error.detail)
            }
          } else {
            errorMessage = JSON.stringify(error)
          }
        } catch {
          const errorText = await response.text()
          errorMessage = errorText || errorMessage
        }
        console.error('Registration error:', errorMessage)
        toast(errorMessage, 'error')
        return
      }

      // Check if response has content before parsing JSON
      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        try {
          const data = await response.json()
          console.log('Registration successful:', data)
        } catch (e) {
          console.log('Registration successful (no JSON response)')
        }
      }
      
      toast('Registration successful! Please sign in.', 'success')
      router.push('/login')
    } catch (error) {
      console.error('Registration error:', error)
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        toast('Cannot connect to server. Is the backend running?', 'error')
      } else {
        toast('An error occurred during registration', 'error')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            Create Account
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Sign up for Bitcoin Estate Planning
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="full_name"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Full Name
            </label>
            <input
              id="full_name"
              type="text"
              value={formData.full_name}
              onChange={(e) =>
                setFormData({ ...formData, full_name: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              placeholder="John Doe"
            />
          </div>

          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Email <span className="text-red-500">*</span>
            </label>
            <input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
              required
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Password <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                required
                minLength={8}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 pr-10"
                placeholder="At least 8 characters"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </button>
            </div>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Password must be at least 8 characters long
            </p>
          </div>

          <Button
            type="submit"
            disabled={isLoading}
            className="w-full"
          >
            {isLoading ? 'Creating account...' : 'Create Account'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
            <a
              href="/login"
              className="text-bitcoin-orange hover:text-bitcoin-orange-dark font-medium"
            >
              Sign in
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}

