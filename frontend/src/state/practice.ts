import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

export type LiveItem = {
  id: string
  teks: string
  type: 'numeric'|'mc'
  seed: number
  stimulus?: any
  prompt: string
  options?: { id: string; text: string }[]
  answer_format?: { form: 'int'|'fraction'|'decimal'; units?: string }
  hints?: string[]
  difficulty: number
}

export type AttemptResult = { correct: boolean; feedbackCode?: string; masteryDelta?: number }

type PracticeState = {
  currentItem: LiveItem | null
  lastResult: AttemptResult | null
  queue: string[]
  timerMs: number
  setCurrentItem: (item: LiveItem) => void
  setResult: (res: AttemptResult) => void
  clearResult: () => void
}

export const usePractice = create<PracticeState>()(
  immer((set) => ({
    currentItem: null,
    lastResult: null,
    queue: [],
    timerMs: 0,
    setCurrentItem: (item) => set((s) => { s.currentItem = item }),
    setResult: (res) => set((s) => { s.lastResult = res }),
    clearResult: () => set((s) => { s.lastResult = null }),
  }))
)


