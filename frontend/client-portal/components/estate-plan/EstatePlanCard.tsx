'use client'

import { EstatePlan } from '@/lib/api'
import { formatDate, copyToClipboard } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Copy, Edit, Trash2, ArrowRight } from 'lucide-react'
import { toast } from '@/components/ui/toast'
import { useRouter } from 'next/navigation'

interface EstatePlanCardProps {
  estatePlan: EstatePlan
  onEdit: (estatePlan: EstatePlan) => void
  onDelete: (id: number) => void
}

export function EstatePlanCard({ estatePlan, onEdit, onDelete }: EstatePlanCardProps) {
  const router = useRouter()
  
  const handleCopyAddress = async () => {
    if (estatePlan.bitcoin_address) {
      await copyToClipboard(estatePlan.bitcoin_address)
      toast('Bitcoin address copied to clipboard', 'success')
    }
  }

  const handleViewDetails = () => {
    router.push(`/estate-plans/${estatePlan.id}`)
  }

  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:shadow-lg transition-all duration-200 transform hover:scale-[1.02] cursor-pointer group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1 group-hover:text-bitcoin-orange transition-colors">
            {estatePlan.name}
          </h3>
          {estatePlan.description && (
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">{estatePlan.description}</p>
          )}
        </div>
        <Badge
          variant={estatePlan.is_active ? 'success' : 'default'}
          size="sm"
        >
          {estatePlan.is_active ? 'Active' : 'Inactive'}
        </Badge>
      </div>

      {estatePlan.bitcoin_address && (
        <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-700/50 rounded border border-gray-200 dark:border-gray-600 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Bitcoin Address</p>
              <p className="text-sm font-mono text-gray-900 dark:text-gray-100 truncate">
                {estatePlan.bitcoin_address}
              </p>
            </div>
            <Button
              variant="outline"
              size="icon"
              onClick={handleCopyAddress}
              className="ml-2 h-8 w-8 flex-shrink-0 border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-600 hover:scale-110 transition-transform"
            >
              <Copy className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}

      <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-4">
        <span>Created: {formatDate(estatePlan.created_at)}</span>
        <span>Updated: {formatDate(estatePlan.updated_at)}</span>
      </div>

      <div className="flex gap-2">
        <Button
          variant="default"
          size="sm"
          onClick={handleViewDetails}
          className="flex-1 hover:scale-105 transition-transform"
        >
          View Details
          <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(estatePlan)}
          className="hover:scale-110 transition-transform"
        >
          <Edit className="h-4 w-4" />
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={() => onDelete(estatePlan.id)}
          className="hover:scale-110 transition-transform"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

