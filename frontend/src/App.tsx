import { NavLink, Outlet, Route, Routes, Navigate, useNavigate } from 'react-router-dom'
import { useEffect } from 'react'
import React from 'react'
import { useSettings } from './state/settings'
import { useAuth } from './state/auth'
import { SkillTile } from './components/SkillTile'
import { ItemPlayer } from './components/ItemPlayer'
import { fetchTeksMap } from './services/api'
import { useMastery } from './state/mastery'

function Layout() {
  const { theme, fontSize, dyslexiaFont } = useSettings()
  const { userId } = useAuth()

  useEffect(() => {
    const root = document.documentElement
    root.classList.toggle('theme-high-contrast', theme === 'high-contrast')
    root.classList.toggle('theme-default', theme === 'default')
    root.classList.toggle('font-S', fontSize === 'S')
    root.classList.toggle('font-M', fontSize === 'M')
    root.classList.toggle('font-L', fontSize === 'L')
    root.classList.toggle('font-dyslexia', dyslexiaFont)
  }, [theme, fontSize, dyslexiaFont])

  if (!userId) {
    return <Navigate to="/signin" replace />
  }

  return (
    <div className="app">
      <nav className="nav" role="navigation" aria-label="Main">
        <NavLink to="/" end aria-label="Home">Home</NavLink>
        <NavLink to="/practice" aria-label="Practice">Practice</NavLink>
        <NavLink to="/review" aria-label="Review">Review</NavLink>
        <NavLink to="/progress" aria-label="Progress">Progress</NavLink>
        <NavLink to="/settings" aria-label="Settings">Settings</NavLink>
      </nav>
      <main className="main" role="main">
        <Outlet />
      </main>
    </div>
  )
}

function Home() {
  const [teksMap, setTeksMap] = React.useState<Record<string, { title: string }>>({})
  const { getMastery } = useMastery()

  React.useEffect(() => {
    fetchTeksMap().then(setTeksMap)
  }, [])

  return (
    <div style={{ display: 'grid', gap: 20 }}>
      <header>
        <h1 style={{ margin: 0, fontSize: 28, color: '#e2e8f0' }}>TEKS Skills</h1>
        <p style={{ margin: '8px 0 0', color: '#94a3b8' }}>Choose a skill to practice</p>
      </header>
      <div style={{ display: 'grid', gap: 12, gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))' }}>
        {Object.entries(teksMap).map(([code, { title }]) => {
          const mastery = getMastery(code)
          return (
            <SkillTile
              key={code}
              teks={code}
              title={title}
              masteryScore={mastery?.score || 0}
              dueReview={mastery?.dueReviewAt ? mastery.dueReviewAt < Date.now() : false}
            />
          )
        })}
      </div>
    </div>
  )
}

function Practice() { return <ItemPlayer /> }
function Review() {
  const [tab, setTab] = React.useState<'due-today' | 'this-week' | 'custom'>('due-today')
  const [selectedSkills, setSelectedSkills] = React.useState<string[]>([])
  const [itemCount, setItemCount] = React.useState<10 | 20 | 30>(10)
  const [teksMap, setTeksMap] = React.useState<Record<string, { title: string }>>({})
  const { records } = useMastery()
  const navigate = useNavigate()

  React.useEffect(() => {
    fetchTeksMap().then(setTeksMap)
  }, [])

  const dueToday = Object.values(records).filter(r => r.dueReviewAt && r.dueReviewAt < Date.now())
  const dueThisWeek = Object.values(records).filter(r => r.dueReviewAt && r.dueReviewAt < Date.now() + 7 * 24 * 60 * 60 * 1000)

  function startCustomReview() {
    if (selectedSkills.length === 0) return
    // TODO: wire to practice mode with selected skills
    navigate('/practice')
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <header>
        <h1 style={{ margin: 0, fontSize: 28, color: '#e2e8f0' }}>Review</h1>
        <p style={{ margin: '8px 0 0', color: '#94a3b8' }}>Spiral practice to keep skills fresh</p>
      </header>

      <div style={{ display: 'flex', gap: 8, borderBottom: '1px solid #334155' }}>
        <TabButton active={tab === 'due-today'} onClick={() => setTab('due-today')}>Due Today ({dueToday.length})</TabButton>
        <TabButton active={tab === 'this-week'} onClick={() => setTab('this-week')}>This Week ({dueThisWeek.length})</TabButton>
        <TabButton active={tab === 'custom'} onClick={() => setTab('custom')}>Custom Set</TabButton>
      </div>

      {tab === 'due-today' && (
        <div style={{ display: 'grid', gap: 12 }}>
          {dueToday.length === 0 ? (
            <div style={{ padding: 40, textAlign: 'center', color: '#94a3b8' }}>🎉 All caught up! No items due today.</div>
          ) : (
            dueToday.map(rec => (
              <ReviewSkillCard key={rec.teks} teks={rec.teks} title={teksMap[rec.teks]?.title || rec.teks} mastery={rec.score} />
            ))
          )}
          {dueToday.length > 0 && (
            <button onClick={() => navigate('/practice')} style={{ marginTop: 12 }}>Start Review</button>
          )}
        </div>
      )}

      {tab === 'this-week' && (
        <div style={{ display: 'grid', gap: 12 }}>
          {dueThisWeek.length === 0 ? (
            <div style={{ padding: 40, textAlign: 'center', color: '#94a3b8' }}>Nothing due this week.</div>
          ) : (
            dueThisWeek.map(rec => (
              <ReviewSkillCard key={rec.teks} teks={rec.teks} title={teksMap[rec.teks]?.title || rec.teks} mastery={rec.score} />
            ))
          )}
          {dueThisWeek.length > 0 && (
            <button onClick={() => navigate('/practice')} style={{ marginTop: 12 }}>Start Review</button>
          )}
        </div>
      )}

      {tab === 'custom' && (
        <div style={{ display: 'grid', gap: 20 }}>
          <div>
            <h3 style={{ margin: '0 0 12px', color: '#e2e8f0' }}>Choose Skills</h3>
            <div style={{ display: 'grid', gap: 8 }}>
              {Object.entries(teksMap).map(([code, { title }]) => {
                const isSelected = selectedSkills.includes(code)
                return (
                  <label key={code} style={{ display: 'flex', gap: 12, alignItems: 'center', padding: '12px 16px', borderRadius: 8, border: '2px solid', borderColor: isSelected ? '#3b82f6' : '#334155', background: isSelected ? 'rgba(59, 130, 246, 0.1)' : '#1e293b', cursor: 'pointer', transition: 'all 0.2s ease' }}>
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => {
                        setSelectedSkills(prev => isSelected ? prev.filter(s => s !== code) : [...prev, code])
                      }}
                      style={{ width: 18, height: 18, cursor: 'pointer' }}
                    />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 600, color: '#3b82f6' }}>{code}</div>
                      <small style={{ color: '#94a3b8' }}>{title}</small>
                    </div>
                  </label>
                )
              })}
            </div>
          </div>

          <div>
            <h3 style={{ margin: '0 0 12px', color: '#e2e8f0' }}>Item Count</h3>
            <div style={{ display: 'flex', gap: 8 }}>
              {([10, 20, 30] as const).map(n => (
                <button
                  key={n}
                  type="button"
                  onClick={() => setItemCount(n)}
                  style={{ flex: 1, background: itemCount === n ? '#3b82f6' : '#475569' }}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>

          <button disabled={selectedSkills.length === 0} onClick={startCustomReview}>
            Start Custom Review ({selectedSkills.length} skills, {itemCount} items)
          </button>
        </div>
      )}
    </div>
  )
}

function TabButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        background: 'transparent',
        color: active ? '#3b82f6' : '#94a3b8',
        borderBottom: active ? '2px solid #3b82f6' : '2px solid transparent',
        borderRadius: 0,
        padding: '12px 16px',
        fontWeight: 500,
        transform: 'none',
        boxShadow: 'none'
      }}
    >
      {children}
    </button>
  )
}

function ReviewSkillCard({ teks, title, mastery }: { teks: string; title: string; mastery: number }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 16, background: '#1e293b', borderRadius: 8, border: '1px solid #334155' }}>
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: 600, color: '#3b82f6' }}>{teks}</div>
        <small style={{ color: '#94a3b8' }}>{title}</small>
      </div>
      <div style={{ width: 100 }}>
        <div style={{ height: 6, background: '#334155', borderRadius: 999 }}>
          <div style={{ width: `${mastery * 100}%`, height: 6, background: '#10b981', borderRadius: 999 }} />
        </div>
      </div>
      <div style={{ width: 40, textAlign: 'right', fontWeight: 600, fontSize: 14 }}>{Math.round(mastery * 100)}%</div>
    </div>
  )
}
function Progress() {
  const { records } = useMastery()
  const totalAttempts = Object.values(records).reduce((sum, r) => sum + r.attempts, 0)
  const avgMastery = Object.values(records).length > 0
    ? Object.values(records).reduce((sum, r) => sum + r.score, 0) / Object.values(records).length
    : 0

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <header>
        <h1 style={{ margin: 0, fontSize: 28, color: '#e2e8f0' }}>Progress</h1>
        <p style={{ margin: '8px 0 0', color: '#94a3b8' }}>Your learning journey</p>
      </header>

      <div style={{ display: 'grid', gap: 12, gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
        <StatCard label="Items Practiced" value={totalAttempts} />
        <StatCard label="Avg Mastery" value={`${Math.round(avgMastery * 100)}%`} />
        <StatCard label="Skills Attempted" value={Object.keys(records).length} />
      </div>

      <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155' }}>
        <h3 style={{ margin: '0 0 16px', color: '#e2e8f0' }}>Skills Overview</h3>
        <div style={{ display: 'grid', gap: 12 }}>
          {Object.values(records).map((rec) => (
            <div key={rec.teks} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, color: '#3b82f6' }}>{rec.teks}</div>
                <small style={{ color: '#94a3b8' }}>{rec.attempts} attempts</small>
              </div>
              <div style={{ width: 200 }}>
                <div style={{ height: 8, background: '#334155', borderRadius: 999 }}>
                  <div style={{ width: `${rec.score * 100}%`, height: 8, background: '#10b981', borderRadius: 999, transition: 'width 0.5s ease' }} />
                </div>
              </div>
              <div style={{ width: 50, textAlign: 'right', fontWeight: 600 }}>{Math.round(rec.score * 100)}%</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155' }}>
      <div style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>{label}</div>
      <div style={{ fontSize: 32, fontWeight: 600, color: '#e2e8f0' }}>{value}</div>
    </div>
  )
}
function Settings() {
  const { theme, setTheme, fontSize, setFontSize, dyslexiaFont, toggleDyslexiaFont, readAloud, toggleReadAloud } = useSettings()
  const { displayName, signOut } = useAuth()
  const navigate = useNavigate()
  
  function handleSignOut() {
    if (confirm('Sign out? Your progress is saved locally.')) {
      signOut()
      navigate('/signin')
    }
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <header>
        <h1 style={{ margin: 0, fontSize: 28, color: '#e2e8f0' }}>Settings</h1>
        <p style={{ margin: '8px 0 0', color: '#94a3b8' }}>Customize your experience</p>
      </header>

      <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155' }}>
        <h3 style={{ margin: '0 0 16px', color: '#e2e8f0' }}>Profile</h3>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
      <div>
            <div style={{ fontWeight: 600, color: '#e2e8f0' }}>{displayName}</div>
            <small style={{ color: '#94a3b8' }}>Signed in</small>
          </div>
          <button type="button" onClick={handleSignOut}>Sign Out</button>
        </div>
      </div>

      <div style={{ background: '#1e293b', padding: 20, borderRadius: 12, border: '1px solid #334155', display: 'grid', gap: 16 }}>
        <h3 style={{ margin: 0, color: '#e2e8f0' }}>Accessibility</h3>
        
        <div>
          <label style={{ marginBottom: 8 }}>Theme</label>
          <select value={theme} onChange={(e) => setTheme(e.target.value as any)}>
            <option value="default">Default (Dark)</option>
            <option value="high-contrast">High Contrast</option>
          </select>
        </div>
        
        <div>
          <label style={{ marginBottom: 8 }}>Text Size</label>
          <select value={fontSize} onChange={(e) => setFontSize(e.target.value as any)}>
            <option value="S">Small</option>
            <option value="M">Medium</option>
            <option value="L">Large</option>
          </select>
        </div>
        
        <label style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '12px 0', cursor: 'pointer' }}>
          <input type="checkbox" checked={dyslexiaFont} onChange={toggleDyslexiaFont} style={{ width: 18, height: 18 }} />
          <div>
            <div style={{ fontWeight: 500, color: '#e2e8f0' }}>Dyslexia‑friendly font</div>
            <small style={{ color: '#94a3b8' }}>Use Atkinson Hyperlegible</small>
          </div>
        </label>
        
        <label style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '12px 0', cursor: 'pointer' }}>
          <input type="checkbox" checked={readAloud} onChange={toggleReadAloud} style={{ width: 18, height: 18 }} />
          <div>
            <div style={{ fontWeight: 500, color: '#e2e8f0' }}>Read‑aloud</div>
            <small style={{ color: '#94a3b8' }}>Hear questions read to you</small>
          </div>
        </label>
      </div>
    </div>
  )
}

function SignIn() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = e.currentTarget
    const name = new FormData(form).get('name')?.toString().trim() || ''
    const lastInitial = new FormData(form).get('lastInitial')?.toString().trim() || ''
    const displayName = lastInitial ? `${name} ${lastInitial}.` : name
    if (displayName) {
      signIn(displayName)
      navigate('/')
    }
  }
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', padding: 20 }}>
      <form onSubmit={onSubmit} aria-label="Sign in" className="fade-in" style={{ display: 'grid', gap: 16, width: '100%', maxWidth: 400, background: '#1e293b', padding: 32, borderRadius: 12, border: '1px solid #334155' }}>
        <h2 style={{ margin: 0, fontSize: 24, color: '#3b82f6' }}>Welcome! 👋</h2>
        <p style={{ margin: 0, color: '#94a3b8' }}>Hi! I'm your math practice buddy.</p>
        <label>
          First name
          <input name="name" required aria-required="true" />
        </label>
        <label>
          Last initial (optional)
          <input name="lastInitial" />
        </label>
        <button type="submit">Start</button>
      </form>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/signin" element={<SignIn />} />
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="practice" element={<Practice />} />
        <Route path="review" element={<Review />} />
        <Route path="progress" element={<Progress />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}
