import React from 'react'
export default function FeatureChips({ features }: { features: string[] }) {
  if (!features?.length) return null
  return (
    <div className="mt-4">
      <div className="text-sm text-gray-600 mb-2">Top contributing n-grams</div>
      <div className="flex flex-wrap gap-2">
        {features.map((f, i) => (
          <span key={i} className="badge bg-gray-100 text-gray-800 border border-gray-200">{f}</span>
        ))}
      </div>
    </div>
  )
}
