import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

export type MasteryRecord = {
  teks: string
  score: number // 0..1
  attempts: number
  lastSeenAt: number
  dueReviewAt?: number
}

type MasteryState = {
  records: Record<string, MasteryRecord>
  setMastery: (teks: string, data: Partial<MasteryRecord>) => void
  getMastery: (teks: string) => MasteryRecord | undefined
}

export const useMastery = create<MasteryState>()(
  persist(
    immer((set, get) => ({
      records: {},
      setMastery: (teks, data) =>
        set((s) => {
          if (!s.records[teks]) {
            s.records[teks] = { teks, score: 0, attempts: 0, lastSeenAt: Date.now() }
          }
          Object.assign(s.records[teks], data)
        }),
      getMastery: (teks) => get().records[teks],
    })),
    { name: 'mastery' }
  )
)
