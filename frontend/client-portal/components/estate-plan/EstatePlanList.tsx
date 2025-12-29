'use client'

import { useState } from 'react'
import { EstatePlan } from '@/lib/api'
import { EstatePlanCard } from './EstatePlanCard'
import { Button } from '@/components/ui/button'
import { EmptyState } from '@/components/ui/empty-state'
import { Plus, Search, FileText } from 'lucide-react'

interface EstatePlanListProps {
  estatePlans: EstatePlan[]
  onCreate: () => void
  onEdit: (estatePlan: EstatePlan) => void
  onDelete: (id: number) => void
}

export function EstatePlanList({ estatePlans, onCreate, onEdit, onDelete }: EstatePlanListProps) {
  const [searchQuery, setSearchQuery] = useState('')

  const filteredPlans = estatePlans.filter(plan =>
    plan.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    plan.description?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Estate Plans</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Manage your Bitcoin estate planning configurations
          </p>
        </div>
        <Button onClick={onCreate}>
          <Plus className="h-4 w-4 mr-2" />
          Create Estate Plan
        </Button>
      </div>

      {/* Search */}
      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search estate plans..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-bitcoin-orange bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          />
        </div>
      </div>

      {/* List */}
      {filteredPlans.length === 0 ? (
        <EmptyState
          icon={FileText}
          title={searchQuery ? 'No matching estate plans' : 'No estate plans yet'}
          description={
            searchQuery
              ? 'Try adjusting your search terms to find what you\'re looking for.'
              : 'Get started by creating your first Bitcoin estate plan. Define beneficiaries, set up timelock policies, and secure your digital assets.'
          }
          action={
            !searchQuery
              ? {
                  label: 'Create Estate Plan',
                  onClick: onCreate,
                }
              : undefined
          }
          className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPlans.map((plan) => (
            <EstatePlanCard
              key={plan.id}
              estatePlan={plan}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}

