import { useNavigate } from 'react-router-dom'

type SkillTileProps = {
  teks: string
  title: string
  masteryScore: number
  dueReview?: boolean
}

export function SkillTile({ teks, title, masteryScore, dueReview }: SkillTileProps) {
  const navigate = useNavigate()
  
  return (
    <button
      onClick={() => navigate(`/practice?teks=${teks}`)}
      style={{
        display: 'grid',
        gap: 12,
        padding: 20,
        background: '#1e293b',
        border: '1px solid #334155',
        borderRadius: 12,
        textAlign: 'left',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        position: 'relative',
      }}
      className="skill-tile"
    >
      {dueReview && (
        <span style={{ position: 'absolute', top: 8, right: 8, background: '#f59e0b', color: 'white', fontSize: 11, fontWeight: 600, padding: '4px 8px', borderRadius: 6 }}>
          Due
        </span>
      )}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, color: '#3b82f6', marginBottom: 4 }}>{teks}</div>
          <div style={{ fontSize: 14, color: '#cbd5e1' }}>{title}</div>
        </div>
        <MasteryRing score={masteryScore} />
      </div>
    </button>
  )
}

function MasteryRing({ score }: { score: number }) {
  const percent = Math.round(score * 100)
  const radius = 28
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score * circumference)
  
  return (
    <div style={{ position: 'relative', width: 70, height: 70 }}>
      <svg width="70" height="70" style={{ transform: 'rotate(-90deg)' }}>
        <circle cx="35" cy="35" r={radius} stroke="#334155" strokeWidth="6" fill="none" />
        <circle
          cx="35"
          cy="35"
          r={radius}
          stroke={score > 0.7 ? '#10b981' : score > 0.3 ? '#3b82f6' : '#94a3b8'}
          strokeWidth="6"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 0.5s ease' }}
        />
      </svg>
      <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 14, fontWeight: 600, color: '#e2e8f0' }}>
        {percent}%
      </div>
    </div>
  )
}
