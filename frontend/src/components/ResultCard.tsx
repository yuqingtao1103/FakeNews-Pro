import React from 'react'
export default function ResultCard({ label, proba }: { label: string; proba: number }) {
  const pct = Math.round(proba * 100)
  const isReal = label === 'real'
  const color = isReal ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
  const barColor = isReal ? 'bg-green-500' : 'bg-red-500'
  return (
    <div className="card">
      <div className="flex items-center gap-3">
        <span className={`badge ${color}`}>{label.toUpperCase()}</span>
        <span className="text-sm text-gray-600">confidence {pct}%</span>
      </div>
      <div className="mt-3 h-2 w-full bg-gray-200 rounded">
        <div className={`h-2 ${barColor} rounded`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}
