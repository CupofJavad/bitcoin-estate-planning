'use client'

import { useState, useEffect } from 'react'
import { useSession, signOut } from 'next-auth/react'
import { EstatePlan, estatePlansApi } from '@/lib/api'
import { EstatePlanList } from '@/components/estate-plan/EstatePlanList'
import { EstatePlanForm } from '@/components/estate-plan/EstatePlanForm'
import { Modal } from '@/components/ui/modal'
import { ToastContainer, toast } from '@/components/ui/toast'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { StatCard } from '@/components/ui/stat-card'
import { AnimatedCounter } from '@/components/ui/animated-counter'
import { Skeleton } from '@/components/ui/skeleton'
import { SuccessAnimation } from '@/components/ui/success-animation'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { FileText, Users, Clock, TrendingUp, LogOut, MessageCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Chatbot } from '@/components/chatbot/Chatbot'

function UserMenu() {
  const { data: session } = useSession()

  if (!session) {
    return null
  }

  return (
    <div className="flex items-center gap-4">
      <span className="text-sm text-gray-600 dark:text-gray-400">
        {session.user?.email}
      </span>
      <Button
        variant="outline"
        size="sm"
        onClick={() => signOut({ callbackUrl: '/login' })}
      >
        <LogOut className="h-4 w-4 mr-2" />
        Sign Out
      </Button>
    </div>
  )
}

export default function Home() {
  const [estatePlans, setEstatePlans] = useState<EstatePlan[]>([])
  const [loading, setLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingPlan, setEditingPlan] = useState<EstatePlan | undefined>()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [showChatbot, setShowChatbot] = useState(false)

  const fetchEstatePlans = async () => {
    try {
      setLoading(true)
      const data = await estatePlansApi.list()
      setEstatePlans(data)
    } catch (error) {
      toast('Failed to load estate plans', 'error')
      console.error('Error fetching estate plans:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEstatePlans()
  }, [])

  const handleCreate = () => {
    setEditingPlan(undefined)
    setIsModalOpen(true)
  }

  const handleEdit = (estatePlan: EstatePlan) => {
    setEditingPlan(estatePlan)
    setIsModalOpen(true)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this estate plan? This action cannot be undone.')) {
      return
    }

    try {
      await estatePlansApi.delete(id)
      setSuccessMessage('Estate plan deleted successfully')
      setShowSuccess(true)
      toast('Estate plan deleted successfully', 'success')
      fetchEstatePlans()
    } catch (error) {
      toast('Failed to delete estate plan', 'error')
      console.error('Error deleting estate plan:', error)
    }
  }

  const handleSubmit = async (data: {
    name: string
    description: string
    bitcoin_address: string
    is_active: boolean
  }) => {
    try {
      setIsSubmitting(true)
      
      if (editingPlan) {
        await estatePlansApi.update(editingPlan.id, {
          ...editingPlan,
          ...data,
          user_id: editingPlan.user_id,
        })
        setSuccessMessage('Estate plan updated successfully')
        toast('Estate plan updated successfully', 'success')
      } else {
        await estatePlansApi.create({
          ...data,
        })
        setSuccessMessage('Estate plan created successfully')
        toast('Estate plan created successfully', 'success')
      }
      
      setIsModalOpen(false)
      setEditingPlan(undefined)
      setShowSuccess(true)
      fetchEstatePlans()
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to save estate plan'
      toast(message, 'error')
      console.error('Error saving estate plan:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Calculate statistics
  const totalPlans = estatePlans.length
  const activePlans = estatePlans.filter(p => p.is_active).length
  // Note: beneficiaries and timelock_policies are loaded separately when viewing plan details
  const totalBeneficiaries = 0 // Will be calculated when plans are loaded with relations
  const avgBeneficiariesPerPlan = '0'

  // Show skeleton loading instead of spinner
  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Header Skeleton */}
            <div className="mb-8">
              <div className="h-8 w-64 bg-gray-200 dark:bg-gray-700 rounded mb-2 animate-pulse"></div>
              <div className="h-4 w-96 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
            </div>
            
            {/* Stats Skeleton */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              {Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                  <div className="flex items-center justify-between mb-2">
                    <div className="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                    <div className="h-5 w-5 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                  </div>
                  <div className="h-8 w-16 bg-gray-200 dark:bg-gray-700 rounded mb-2 animate-pulse"></div>
                  <div className="h-3 w-20 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                </div>
              ))}
            </div>
            
            {/* List Skeleton */}
            <div className="space-y-3">
              {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="h-6 w-48 bg-gray-200 dark:bg-gray-700 rounded mb-2 animate-pulse"></div>
                      <div className="h-4 w-32 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                    </div>
                    <div className="h-8 w-8 bg-gray-200 dark:bg-gray-700 rounded-full animate-pulse"></div>
                  </div>
                  <div className="h-4 w-full bg-gray-200 dark:bg-gray-700 rounded mb-2 animate-pulse"></div>
                  <div className="h-4 w-3/4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </ProtectedRoute>
    )
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <SuccessAnimation 
          show={showSuccess} 
          message={successMessage}
          onComplete={() => setShowSuccess(false)}
        />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
              Bitcoin Estate Planning Platform
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Manage your Bitcoin estate plans, beneficiaries, and timelock policies
            </p>
          </div>
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowChatbot(!showChatbot)}
            >
              <MessageCircle className="h-4 w-4 mr-2" />
              Assistant
            </Button>
            <ThemeToggle />
            <UserMenu />
          </div>
        </div>

        {/* Dashboard Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            title="Total Estate Plans"
            value={totalPlans}
            icon={FileText}
            description={`${activePlans} active`}
          />
          <StatCard
            title="Active Plans"
            value={activePlans}
            icon={TrendingUp}
            description={`${totalPlans > 0 ? ((activePlans / totalPlans) * 100).toFixed(0) : 0}% of total`}
          />
          <StatCard
            title="Total Beneficiaries"
            value={totalBeneficiaries}
            icon={Users}
            description={`${avgBeneficiariesPerPlan} per plan`}
          />
          <StatCard
            title="Timelock Policies"
            value={0}
            icon={Clock}
            description="Across all plans"
          />
        </div>

        {/* Estate Plans List */}
        <EstatePlanList
          estatePlans={estatePlans}
          onCreate={handleCreate}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />

        {/* Create/Edit Modal */}
        <Modal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false)
            setEditingPlan(undefined)
          }}
          title={editingPlan ? 'Edit Estate Plan' : 'Create Estate Plan'}
          size="lg"
        >
          <EstatePlanForm
            estatePlan={editingPlan}
            onSubmit={handleSubmit}
            onCancel={() => {
              setIsModalOpen(false)
              setEditingPlan(undefined)
            }}
            isLoading={isSubmitting}
          />
        </Modal>

        {/* Toast Notifications */}
        <ToastContainer />
        </div>
      </div>

      {/* Chatbot Modal */}
      {showChatbot && (
        <div className="fixed bottom-4 right-4 w-96 h-[600px] z-50">
          <Chatbot onClose={() => setShowChatbot(false)} />
        </div>
      )}
    </ProtectedRoute>
  )
}
