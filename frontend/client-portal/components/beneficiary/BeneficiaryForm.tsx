'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Beneficiary, bitcoinApi } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Tooltip } from '@/components/ui/tooltip'
import { HelpCircle, CheckCircle2, XCircle, Loader2 } from 'lucide-react'

interface BeneficiaryFormData {
  name: string
  email: string
  bitcoin_address: string
  allocation_percentage: number
}

interface BeneficiaryFormProps {
  beneficiary?: Beneficiary
  estatePlanId: number
  totalAllocation: number
  onSubmit: (data: BeneficiaryFormData) => Promise<void>
  onCancel: () => void
  isLoading?: boolean
}

export function BeneficiaryForm({ 
  beneficiary, 
  estatePlanId, 
  totalAllocation,
  onSubmit, 
  onCancel, 
  isLoading 
}: BeneficiaryFormProps) {
  const [addressValidation, setAddressValidation] = useState<{ valid: boolean; errors: string[] } | null>(null)
  const [validatingAddress, setValidatingAddress] = useState(false)
  
  const { register, handleSubmit, formState: { errors }, watch, reset } = useForm<BeneficiaryFormData>({
    defaultValues: {
      name: beneficiary?.name || '',
      email: beneficiary?.email || '',
      bitcoin_address: beneficiary?.bitcoin_address || '',
      allocation_percentage: beneficiary?.allocation_percentage || 0,
    },
  })

  const allocationPercentage = watch('allocation_percentage')
  const bitcoinAddress = watch('bitcoin_address')

  // Validate Bitcoin address when it changes
  useEffect(() => {
    const validateAddress = async () => {
      if (!bitcoinAddress || bitcoinAddress.trim() === '') {
        setAddressValidation(null)
        return
      }

      setValidatingAddress(true)
      try {
        const result = await bitcoinApi.validateAddress(bitcoinAddress)
        setAddressValidation({
          valid: result.valid,
          errors: result.errors,
        })
      } catch (error) {
        setAddressValidation({
          valid: false,
          errors: ['Failed to validate address'],
        })
      } finally {
        setValidatingAddress(false)
      }
    }

    // Debounce validation
    const timeoutId = setTimeout(validateAddress, 500)
    return () => clearTimeout(timeoutId)
  }, [bitcoinAddress])
  // Calculate remaining allocation: 100% - (current total - this beneficiary's current allocation if editing)
  const currentBeneficiaryAllocation = beneficiary ? Number(beneficiary.allocation_percentage) : 0
  const remainingAllocation = 100 - (totalAllocation - currentBeneficiaryAllocation)
  const maxAllocation = Math.max(0, remainingAllocation)

  useEffect(() => {
    if (beneficiary) {
      reset({
        name: beneficiary.name,
        email: beneficiary.email || '',
        bitcoin_address: beneficiary.bitcoin_address || '',
        allocation_percentage: Number(beneficiary.allocation_percentage),
      })
    } else {
      // Reset form when creating new beneficiary
      reset({
        name: '',
        email: '',
        bitcoin_address: '',
        allocation_percentage: 0,
      })
    }
  }, [beneficiary, reset])

  const onSubmitForm = async (data: BeneficiaryFormData) => {
    // Validate total allocation doesn't exceed 100%
    // New total = current total - this beneficiary's current allocation (if editing) + new allocation
    const currentAllocation = beneficiary ? Number(beneficiary.allocation_percentage) : 0
    const newTotal = totalAllocation - currentAllocation + Number(data.allocation_percentage)
    
    if (newTotal > 100.01) { // Allow small floating point tolerance
      const maxAllowed = Math.max(0, 100 - (totalAllocation - currentAllocation))
      alert(`Total allocation cannot exceed 100%. Maximum allowed: ${maxAllowed.toFixed(2)}%`)
      return
    }
    await onSubmit(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Name <span className="text-red-500">*</span>
        </label>
        <input
          id="name"
          type="text"
          {...register('name', { required: 'Name is required' })}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email', {
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Invalid email address',
            },
          })}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="bitcoin_address" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Bitcoin Address
        </label>
        <div className="relative">
          <input
            id="bitcoin_address"
            type="text"
            {...register('bitcoin_address')}
            placeholder="bc1q... or tb1q..."
            className={`w-full px-3 py-2 pr-10 border rounded-md focus:outline-none focus:ring-2 font-mono text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 ${
              addressValidation?.valid
                ? 'border-green-500 focus:ring-green-500'
                : addressValidation?.valid === false
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 dark:border-gray-600 focus:ring-bitcoin-orange'
            }`}
          />
          {bitcoinAddress && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2">
              {validatingAddress ? (
                <Loader2 className="h-4 w-4 text-gray-400 animate-spin" />
              ) : addressValidation?.valid ? (
                <CheckCircle2 className="h-4 w-4 text-green-500" />
              ) : addressValidation?.valid === false ? (
                <XCircle className="h-4 w-4 text-red-500" />
              ) : null}
            </div>
          )}
        </div>
        {addressValidation?.valid === false && addressValidation.errors.length > 0 && (
          <div className="mt-1">
            {addressValidation.errors.map((error, index) => (
              <p key={index} className="text-xs text-red-600 dark:text-red-400">
                {error}
              </p>
            ))}
          </div>
        )}
        {addressValidation?.valid && (
          <p className="mt-1 text-xs text-green-600 dark:text-green-400">
            Valid Bitcoin address
          </p>
        )}
        {!bitcoinAddress && (
          <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Optional: Bitcoin address where this beneficiary will receive funds
          </p>
        )}
      </div>

      <div>
        <label htmlFor="allocation_percentage" className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Allocation Percentage <span className="text-red-500">*</span>
          <Tooltip content="The percentage of the estate this beneficiary will receive. Total allocation cannot exceed 100%.">
            <HelpCircle className="h-4 w-4 text-gray-400 cursor-help" />
          </Tooltip>
        </label>
        <div className="flex items-center gap-3">
          <input
            id="allocation_percentage"
            type="number"
            step="0.01"
            min="0"
            max={maxAllocation}
            {...register('allocation_percentage', {
              required: 'Allocation percentage is required',
              min: { value: 0, message: 'Must be at least 0%' },
              max: { value: maxAllocation, message: `Maximum ${maxAllocation.toFixed(2)}% available` },
            })}
            className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          />
          <span className="text-gray-600">%</span>
        </div>
        {errors.allocation_percentage && (
          <p className="mt-1 text-sm text-red-600">{errors.allocation_percentage.message}</p>
        )}
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Remaining allocation: {remainingAllocation.toFixed(2)}%
        </p>
        {allocationPercentage && (
          <div className="mt-2">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${Math.min(allocationPercentage, 100)}%` }}
              />
            </div>
          </div>
        )}
      </div>

      <div className="flex gap-3 pt-4">
        <Button
          type="submit"
          disabled={isLoading}
          className="flex-1"
        >
          {isLoading ? 'Saving...' : beneficiary ? 'Update' : 'Create'}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isLoading}
          className="flex-1"
        >
          Cancel
        </Button>
      </div>
    </form>
  )
}

