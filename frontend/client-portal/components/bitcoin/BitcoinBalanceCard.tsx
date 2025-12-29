'use client'

import { useState, useEffect, useCallback } from 'react'
import { bitcoinApi, BitcoinBalance } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { RefreshCw, Copy, Check, Loader2, AlertCircle } from 'lucide-react'
import { toast } from '@/components/ui/toast'

interface BitcoinBalanceCardProps {
  address: string
}

export function BitcoinBalanceCard({ address }: BitcoinBalanceCardProps) {
  const [balance, setBalance] = useState<BitcoinBalance | null>(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const fetchBalance = useCallback(async (useCache = true) => {
    if (!address) return

    setLoading(true)
    try {
      const data = await bitcoinApi.getBalance(address, useCache)
      setBalance(data)
      if (data.error) {
        toast(data.error, 'error')
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to fetch balance'
      toast(message, 'error')
      console.error('Error fetching balance:', error)
    } finally {
      setLoading(false)
    }
  }, [address])

  useEffect(() => {
    if (address) {
      fetchBalance(true)
    }
  }, [address, fetchBalance])

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(address)
      setCopied(true)
      toast('Address copied to clipboard', 'success')
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      toast('Failed to copy address', 'error')
    }
  }

  const formatBTC = (btc: number) => {
    if (btc === 0) return '0.00000000'
    if (btc < 0.00001) return btc.toFixed(8)
    return btc.toFixed(8).replace(/\.?0+$/, '')
  }

  const formatSats = (sats: number) => {
    return new Intl.NumberFormat('en-US').format(sats)
  }

  if (!address) {
    return null
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">
            Bitcoin Balance
          </h3>
          <div className="flex items-center gap-2">
            <p className="text-sm font-mono text-gray-600 dark:text-gray-400 break-all">
              {address}
            </p>
            <button
              onClick={handleCopy}
              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              title="Copy address"
            >
              {copied ? (
                <Check className="h-4 w-4 text-green-500" />
              ) : (
                <Copy className="h-4 w-4 text-gray-400" />
              )}
            </button>
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => fetchBalance(false)}
          disabled={loading}
        >
          {loading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <RefreshCw className="h-4 w-4" />
          )}
        </Button>
      </div>

      {loading && !balance ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="h-6 w-6 animate-spin text-bitcoin-orange" />
        </div>
      ) : balance?.error ? (
        <div className="flex items-center gap-2 text-red-600 dark:text-red-400 py-4">
          <AlertCircle className="h-5 w-5" />
          <p className="text-sm">{balance.error}</p>
        </div>
      ) : balance ? (
        <div className="space-y-3">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Balance</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {formatBTC(balance.balance_btc)} BTC
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {formatSats(balance.balance_sats)} sats
            </p>
          </div>
          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-700">
            <span>
              {balance.cached ? 'Cached' : 'Live'} data
              {balance.provider && ` • ${balance.provider}`}
            </span>
            {balance.last_updated && (
              <span>
                Updated: {new Date(balance.last_updated).toLocaleTimeString()}
              </span>
            )}
          </div>
        </div>
      ) : null}
    </div>
  )
}

