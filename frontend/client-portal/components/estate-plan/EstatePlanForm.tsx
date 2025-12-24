'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { EstatePlan } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Tooltip } from '@/components/ui/tooltip'
import { HelpCircle } from 'lucide-react'

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
  const { register, handleSubmit, formState: { errors }, reset } = useForm<EstatePlanFormData>({
    defaultValues: {
      name: estatePlan?.name || '',
      description: estatePlan?.description || '',
      bitcoin_address: estatePlan?.bitcoin_address || '',
      is_active: estatePlan?.is_active ?? true,
    },
  })

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
        <input
          id="bitcoin_address"
          type="text"
          {...register('bitcoin_address')}
          placeholder="bc1q..."
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange font-mono text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        />
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Enter a Bitcoin address for this estate plan
        </p>
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

