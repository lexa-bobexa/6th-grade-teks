import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type AuthState = {
  userId: string | null
  displayName: string | null
  lastSeenAt: number | null
  signIn: (displayName: string) => void
  signOut: () => void
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      userId: null,
      displayName: null,
      lastSeenAt: null,
      signIn: (displayName: string) => {
        const userId = `u_${Math.random().toString(36).slice(2, 10)}`
        set({ userId, displayName, lastSeenAt: Date.now() })
      },
      signOut: () => set({ userId: null, displayName: null, lastSeenAt: null }),
    }),
    { name: 'auth' }
  )
)


