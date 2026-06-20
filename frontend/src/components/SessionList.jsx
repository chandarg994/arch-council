import { useState, useEffect } from 'react'

const STATUS_COLORS = {
  complete: '#34d399',
  queued: '#8892a4',
  stage1_council: '#6c8cff',
  stage2_review: '#a78bfa',
  stage3_synthesis: '#fbbf24',
  stage4_ratchet: '#34d399',
  stage5_finalizing: '#6c8cff',
}

export default function SessionList({ onSelect }) {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/sessions')
      .then(r => r.json())
      .then(data => { setSessions(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div style={{ color: 'var(--text-muted)', padding: 20 }}>Loading sessions...</div>

  if (sessions.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
        <div style={{ fontSize: 32, marginBottom: 12 }}>📂</div>
        No sessions yet. Submit a requirement to get started.
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <h2 style={{ fontWeight: 600, marginBottom: 16 }}>Session History</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {sessions.map(s => {
          const color = STATUS_COLORS[s.status] || '#8892a4'
          return (
            <div
              key={s.id}
              onClick={() => onSelect(s.id)}
              style={{
                background: 'var(--surface)', border: '1px solid var(--border)',
                borderRadius: 10, padding: '14px 18px', cursor: 'pointer',
                display: 'flex', alignItems: 'center', gap: 14,
                transition: 'border-color 0.15s',
              }}
              onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--accent)'}
              onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
            >
              <div style={{ width: 8, height: 8, borderRadius: '50%', background: color, flexShrink: 0 }} />
              <div style={{ flex: 1 }}>
                <span style={{ fontWeight: 500 }}>{s.industry}</span>
                <span style={{ color: 'var(--text-muted)', fontSize: 12, marginLeft: 10 }}>
                  {new Date(s.created_at).toLocaleString()}
                </span>
              </div>
              <div style={{ fontSize: 12, color, fontWeight: 500 }}>{s.status}</div>
              {s.best_score != null && (
                <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--warning)', minWidth: 50, textAlign: 'right' }}>
                  {s.best_score.toFixed(0)}/100
                </div>
              )}
              <div style={{ fontSize: 12, color: 'var(--accent)' }}>→</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
