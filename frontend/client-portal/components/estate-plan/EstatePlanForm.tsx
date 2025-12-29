'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { EstatePlan, bitcoinApi } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Tooltip } from '@/components/ui/tooltip'
import { HelpCircle, CheckCircle2, XCircle, Loader2 } from 'lucide-react'

interface EstatePlanFormData {
  name: string
  description: string
  bitcoin_address: string
  is_active: boolean
}

interface EstatePlanFormProps {
  estatePlan?: EstatePlan
  onSubmit: (data: EstatePlanFormData) => Promise<void>
  onCancel: () => void
  isLoading?: boolean
}

export function EstatePlanForm({ estatePlan, onSubmit, onCancel, isLoading }: EstatePlanFormProps) {
  const [addressValidation, setAddressValidation] = useState<{ valid: boolean; errors: string[] } | null>(null)
  const [validatingAddress, setValidatingAddress] = useState(false)
  
  const { register, handleSubmit, formState: { errors }, reset, watch } = useForm<EstatePlanFormData>({
    defaultValues: {
      name: estatePlan?.name || '',
      description: estatePlan?.description || '',
      bitcoin_address: estatePlan?.bitcoin_address || '',
      is_active: estatePlan?.is_active ?? true,
    },
  })

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

  useEffect(() => {
    if (estatePlan) {
      reset({
        name: estatePlan.name,
        description: estatePlan.description || '',
        bitcoin_address: estatePlan.bitcoin_address || '',
        is_active: estatePlan.is_active,
      })
    }
  }, [estatePlan, reset])

  const onSubmitForm = async (data: EstatePlanFormData) => {
    await onSubmit(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-4">
      <div>
        <label htmlFor="name" className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Name <span className="text-red-500">*</span>
          <Tooltip content="A descriptive name for your estate plan (e.g., 'Main Bitcoin Estate')">
            <HelpCircle className="h-4 w-4 text-gray-400 cursor-help" />
          </Tooltip>
        </label>
        <input
          id="name"
          type="text"
          {...register('name', { required: 'Name is required' })}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.name.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="description" className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Description
          <Tooltip content="Optional details about this estate plan">
            <HelpCircle className="h-4 w-4 text-gray-400 cursor-help" />
          </Tooltip>
        </label>
        <textarea
          id="description"
          {...register('description')}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        />
      </div>

      <div>
        <label htmlFor="bitcoin_address" className="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Bitcoin Address
          <Tooltip content="The Bitcoin address associated with this estate plan. Must be a valid P2PKH, P2SH, or Bech32 address.">
            <HelpCircle className="h-4 w-4 text-gray-400 cursor-help" />
          </Tooltip>
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
            Enter a Bitcoin address for this estate plan (optional)
          </p>
        )}
      </div>

      <div className="flex items-center gap-2">
        <input
          id="is_active"
          type="checkbox"
          {...register('is_active')}
          className="h-4 w-4 text-bitcoin-orange focus:ring-bitcoin-orange border-gray-300 dark:border-gray-600 rounded"
        />
        <label htmlFor="is_active" className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
          Active
          <Tooltip content="Only active estate plans will be processed for inheritance">
            <HelpCircle className="h-4 w-4 text-gray-400 cursor-help" />
          </Tooltip>
        </label>
      </div>

      <div className="flex gap-3 pt-4">
        <Button
          type="submit"
          disabled={isLoading}
          className="flex-1"
        >
          {isLoading ? 'Saving...' : estatePlan ? 'Update' : 'Create'}
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

