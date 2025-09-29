import type { LiveItem } from '../state/practice'

// const API_BASE = '/api'

const TEKS_MAP = {
  "6.2": { title: "Rational Numbers & Operations" },
  "6.4": { title: "Proportionality & Unit Rate" },
  "6.7B": { title: "Expressions vs Equations" },
  "6.8B": { title: "Area of a Trapezoid" },
  "6.9A": { title: "One-Step Equations" }
}

export async function fetchTeksMap(): Promise<typeof TEKS_MAP> {
  return TEKS_MAP
}

export async function fetchNextItem(): Promise<LiveItem> {
  try {
    const res = await fetch(`/api/practice/next`)
    if (!res.ok) throw new Error('bad status')
    const data = await res.json()
    return data
  } catch {
    return {
      id: 'sample-1', teks: '6.7B', type: 'numeric', seed: 1,
      prompt: 'What is $8 \\times 6$?', difficulty: 1, hints: ['Think of 8 groups of 6', 'Add: $6+6+6+6+6+6+6+6$'],
    }
  }
}

export async function submitAttempt(payload: { itemId: string; response: any; timeMs: number; usedHint?: boolean }): Promise<{ correct: boolean }> {
  try {
    const res = await fetch(`/api/attempts`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    })
    if (!res.ok) throw new Error('bad status')
    return await res.json()
  } catch {
    const correct = payload.response === 48
    return { correct }
  }
}