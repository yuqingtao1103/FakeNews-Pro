import React, { useEffect, useState } from 'react'
import { health, predict, feedback } from './api'
import ResultCard from './components/ResultCard'
import FeatureChips from './components/FeatureChips'

export default function App() {
  const [headline, setHeadline] = useState('')
  const [body, setBody] = useState('')
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<{ label: string; proba: number; top_features: string[] } | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [server, setServer] = useState<any>(null)

  useEffect(() => { health().then(setServer).catch(() => setServer(null)) }, [])

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault(); setBusy(true); setError(null); setResult(null)
    try {
      const data = await predict({ headline, body })
      setResult(data)
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Something went wrong.')
    } finally {
      setBusy(false)
    }
  }

  async function sendFeedback(correct_label: 'fake' | 'real') {
    if (!result) return
    await feedback({ headline, body, predicted: result.label, correct_label })
    alert('Thanks! Feedback saved.')
  }

  const canSubmit = headline.trim().length > 0 || body.trim().length > 0

  return (
    <div className="container">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold">Fake News Detector</h1>
        <p className="text-gray-600 text-sm">Baseline: TF-IDF + Logistic Regression</p>
        {server && <p className="text-xs text-gray-500 mt-1">API ready · rate {server.rate_limit_per_min}/min</p>}
      </header>

      <form className="card space-y-4" onSubmit={onSubmit}>
        <div>
          <label className="block text-sm font-medium text-gray-700">Headline (optional)</label>
          <input value={headline} onChange={(e) => setHeadline(e.target.value)} className="mt-1 w-full border rounded-xl p-3 focus:outline-none focus:ring" placeholder="Paste a headline" maxLength={300} />
          <p className="text-xs text-gray-500 mt-1">{headline.length}/300</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Article body (optional)</label>
          <textarea value={body} onChange={(e) => setBody(e.target.value)} className="mt-1 w-full border rounded-xl p-3 h-40 resize-y focus:outline-none focus:ring" placeholder="Paste the article text" maxLength={10000} />
          <p className="text-xs text-gray-500 mt-1">{body.length}/10000</p>
        </div>
        <div className="flex items-center gap-3">
          <button disabled={!canSubmit || busy} className="btn" type="submit">{busy ? 'Analyzing…' : 'Analyze'}</button>
          {!canSubmit && <span className="text-xs text-gray-500">Enter a headline or article text</span>}
        </div>
        {error && <div className="text-sm text-red-600">{error}</div>}
      </form>

      {result && (
        <div className="mt-6 space-y-4">
          <ResultCard label={result.label} proba={result.proba} />
          <div className="card">
            <FeatureChips features={result.top_features} />
            <div className="mt-4 flex items-center gap-2">
              <span className="text-sm text-gray-600">Was this correct?</span>
              <button className="btn" onClick={() => sendFeedback('real')}>Mark REAL</button>
              <button className="btn" onClick={() => sendFeedback('fake')}>Mark FAKE</button>
            </div>
          </div>
        </div>
      )}

      <footer className="mt-10 text-xs text-gray-500">
        <p>This is a probabilistic classifier for demonstration. It’s not a fact checker.</p>
      </footer>
    </div>
  )
}
