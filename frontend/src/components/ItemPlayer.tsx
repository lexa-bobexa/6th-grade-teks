import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { usePractice } from '../state/practice'
import { useMastery } from '../state/mastery'
import { fetchNextItem, submitAttempt } from '../services/api'
import { HintModal } from './HintModal'
import { MasteryBar } from './MasteryBar'
import { MathText } from './MathText'

export function ItemPlayer() {
  const [searchParams] = useSearchParams()
  const teksParam = searchParams.get('teks')
  
  const { currentItem, setCurrentItem, lastResult, setResult, clearResult } = usePractice()
  const { getMastery, setMastery } = useMastery()
  const [input, setInput] = useState<string>('')
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [usedHint, setUsedHint] = useState(false)
  const [hintOpen, setHintOpen] = useState(false)
  
  const currentMastery = currentItem ? getMastery(currentItem.teks) : undefined

  useEffect(() => {
    if (!currentItem || (teksParam && currentItem.teks !== teksParam)) {
      fetchNextItem(teksParam || undefined).then(setCurrentItem)
    }
  }, [currentItem, setCurrentItem, teksParam])

  useEffect(() => {
    setInput('')
    setSelected(new Set())
    clearResult()
    setUsedHint(false)
  }, [currentItem, clearResult])

  const canSubmit = useMemo(() => {
    if (!currentItem) return false
    if (currentItem.type === 'numeric') return input.trim().length > 0
    if (currentItem.type === 'mc') return selected.size > 0
    return false
  }, [currentItem, input, selected])

  async function onSubmit() {
    if (!currentItem) return
    const response = currentItem.type === 'numeric' ? Number(input) : Array.from(selected)
    const { correct } = await submitAttempt({ itemId: currentItem.id, response, timeMs: 0, usedHint })
    
    // Update mastery
    const currentScore = currentMastery?.score || 0
    const attempts = (currentMastery?.attempts || 0) + 1
    const delta = correct ? 0.03 : -0.01
    const newScore = Math.max(0, Math.min(1, currentScore + delta))
    
    setMastery(currentItem.teks, {
      score: newScore,
      attempts,
      lastSeenAt: Date.now(),
      dueReviewAt: Date.now() + 7 * 24 * 60 * 60 * 1000 // 7 days later
    })
    
    setResult({ correct, masteryDelta: delta })
    
    if (correct) {
      // Load next after brief delay
      setTimeout(async () => {
        const next = await fetchNextItem(currentItem.teks)
        setCurrentItem(next)
      }, 1000)
    }
  }

  if (!currentItem) return <div>Loading…</div>

  return (
    <div className="fade-in" style={{ display: 'grid', gap: 20, background: '#1e293b', padding: 24, borderRadius: 12, border: '1px solid #334155' }}>
      <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
        <div>
          <div style={{ fontWeight: 600, fontSize: 18, color: '#3b82f6' }}>{currentItem.teks}</div>
          <small style={{ color: '#94a3b8' }}>Difficulty {currentItem.difficulty}</small>
        </div>
        <MasteryBar score={currentMastery?.score || 0} />
      </header>

      {lastResult && (
        <div className={lastResult.correct ? 'bounce' : 'shake'} aria-live="polite" style={{ padding: 12, borderRadius: 8, background: lastResult.correct ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', color: lastResult.correct ? '#10b981' : '#ef4444', fontWeight: 500, textAlign: 'center' }}>
          {lastResult.correct ? '🎉 Nice! +3%' : '💡 Close! Try a hint?'}
        </div>
      )}

      {/* Show SVG diagram if available */}
      {currentItem.stimulus?.diagram?.svg && (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 32, background: '#f8fafc', borderRadius: 12, border: '2px solid #cbd5e1', minHeight: 200 }}>
          <div dangerouslySetInnerHTML={{ __html: currentItem.stimulus.diagram.svg }} />
        </div>
      )}

      <MathText style={{ fontSize: 16, lineHeight: 1.6 }}>{currentItem.prompt}</MathText>

      {currentItem.type === 'numeric' && (
        <input inputMode="numeric" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Enter answer" />
      )}

      {currentItem.type === 'mc' && (
        <div style={{ display: 'grid', gap: 10 }}>
          {currentItem.options?.map((opt) => {
            const active = selected.has(opt.id)
            return (
              <label key={opt.id} style={{ display: 'flex', gap: 12, alignItems: 'center', padding: '14px 16px', borderRadius: 8, border: '2px solid', borderColor: active ? '#3b82f6' : '#334155', background: active ? 'rgba(59, 130, 246, 0.1)' : '#0f172a', cursor: 'pointer', transition: 'all 0.2s ease' }}>
                <input
                  type="checkbox"
                  checked={active}
                  onChange={() => {
                    const next = new Set(selected)
                    if (active) next.delete(opt.id); else next.add(opt.id)
                    setSelected(next)
                  }}
                  style={{ width: 18, height: 18, cursor: 'pointer' }}
                />
                <span style={{ flex: 1 }}>{opt.text}</span>
              </label>
            )
          })}
        </div>
      )}

      <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
        <button type="button" onClick={() => { setUsedHint(true); setHintOpen(true) }} aria-expanded={hintOpen}>💡 Hint</button>
        <button disabled={!canSubmit} onClick={onSubmit} style={{ flex: 1 }}>{lastResult?.correct ? 'Next ➜' : 'Submit'}</button>
      </div>
      <HintModal open={hintOpen} onOpenChange={setHintOpen} hints={currentItem.hints || []} />
    </div>
  )
}


