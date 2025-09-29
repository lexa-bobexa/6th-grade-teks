import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export type Theme = 'default' | 'high-contrast'
export type FontSize = 'S' | 'M' | 'L'

type SettingsState = {
  theme: Theme
  fontSize: FontSize
  dyslexiaFont: boolean
  readAloud: boolean
  setTheme: (theme: Theme) => void
  setFontSize: (size: FontSize) => void
  toggleDyslexiaFont: () => void
  toggleReadAloud: () => void
}

export const useSettings = create<SettingsState>()(
  persist(
    (set) => ({
      theme: 'default',
      fontSize: 'M',
      dyslexiaFont: false,
      readAloud: false,
      setTheme: (theme) => set({ theme }),
      setFontSize: (fontSize) => set({ fontSize }),
      toggleDyslexiaFont: () => set((s) => ({ dyslexiaFont: !s.dyslexiaFont })),
      toggleReadAloud: () => set((s) => ({ readAloud: !s.readAloud })),
    }),
    { name: 'app-settings' }
  )
)


