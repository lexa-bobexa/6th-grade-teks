export function MasteryBar({ score }: { score: number }) {
  const clamped = Math.max(0, Math.min(1, score))
  const percent = Math.round(clamped * 100)
  return (
    <div aria-label={`Mastery ${percent}%`} style={{ width: 160 }}>
      <div style={{ height: 6, background: '#e5e7eb', borderRadius: 999 }}>
        <div style={{ width: `${percent}%`, height: 6, background: '#10b981', borderRadius: 999 }} />
      </div>
    </div>
  )
}


