import { useState } from 'react'
import MarkdownWithMermaid from './MarkdownWithMermaid'

const AGENT_COLORS = {
  business_architect: '#6c8cff',
  data_architect: '#34d399',
  application_architect: '#a78bfa',
  technology_architect: '#fbbf24',
  ai_ml_specialist: '#f472b6',
  risk_governance: '#f87171',
}

const AGENT_ICONS = {
  business_architect: '🏢',
  data_architect: '🗄️',
  application_architect: '⚙️',
  technology_architect: '☁️',
  ai_ml_specialist: '🤖',
  risk_governance: '🛡️',
}

export default function CouncilView({ opinions, reviews, initialDraft, initialScore, loading }) {
  const [activeAgent, setActiveAgent] = useState(null)
  const [showDraft, setShowDraft] = useState(false)

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div style={{ fontSize: 32, marginBottom: 16 }}>🏛️</div>
        <div style={{ color: 'var(--accent)', fontWeight: 600, marginBottom: 8 }}>
          Council in session...
        </div>
        <div style={{ color: 'var(--text-muted)', fontSize: 13 }}>
          6 specialized architects are independently analyzing the requirement
        </div>
        <LoadingDots />
      </div>
    )
  }

  if (opinions.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
        Waiting for council to convene...
      </div>
    )
  }

  const active = activeAgent ? opinions.find(o => o.agent_id === activeAgent) : null

  return (
    <div>
      {/* Agent Tabs */}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 20 }}>
        {opinions.map(op => (
          <AgentChip
            key={op.agent_id}
            opinion={op}
            active={activeAgent === op.agent_id}
            onClick={() => setActiveAgent(activeAgent === op.agent_id ? null : op.agent_id)}
          />
        ))}
        {initialDraft && (
          <button
            onClick={() => { setShowDraft(!showDraft); setActiveAgent(null) }}
            style={{
              background: showDraft ? '#fbbf2422' : 'var(--surface2)',
              border: `1px solid ${showDraft ? '#fbbf24' : 'var(--border)'}`,
              color: showDraft ? '#fbbf24' : 'var(--text-muted)',
              borderRadius: 8, padding: '8px 16px', cursor: 'pointer', fontSize: 12, fontWeight: 500,
            }}
          >
            ⚗️ Initial Draft {initialScore && `(${initialScore.total.toFixed(0)}/100)`}
          </button>
        )}
      </div>

      {/* Opinion Detail */}
      {active && !showDraft && (
        <OpinionPanel opinion={active} reviews={reviews} />
      )}

      {/* Initial Draft */}
      {showDraft && initialDraft && (
        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <div>
              <span style={{ fontWeight: 600 }}>⚗️ Chairman's Initial Synthesis</span>
              <span style={{ color: 'var(--text-muted)', fontSize: 12, marginLeft: 8 }}>
                Before ratchet refinement
              </span>
            </div>
            {initialScore && <ScoreBadge score={initialScore} />}
          </div>
          <MarkdownWithMermaid content={initialDraft} />
        </div>
      )}

      {/* Default: Grid of all opinions */}
      {!active && !showDraft && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: 16 }}>
          {opinions.map(op => (
            <OpinionCard
              key={op.agent_id}
              opinion={op}
              onClick={() => setActiveAgent(op.agent_id)}
            />
          ))}
        </div>
      )}

      {/* Cross-Review Summary */}
      {reviews.length > 0 && !active && !showDraft && (
        <div style={{ marginTop: 24, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: 20 }}>
          <h3 style={{ fontWeight: 600, marginBottom: 12, fontSize: 14 }}>🔍 Cross-Review Summary</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 12 }}>
            {reviews.map(r => (
              <div key={r.reviewer_id} style={{ background: 'var(--surface2)', borderRadius: 8, padding: 12 }}>
                <div style={{ fontWeight: 600, fontSize: 12, marginBottom: 6, color: AGENT_COLORS[r.reviewer_id] }}>
                  {AGENT_ICONS[r.reviewer_id]} {r.reviewer_name}
                </div>
                {r.gaps_identified.length > 0 && (
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                    <strong>Gaps:</strong> {r.gaps_identified.slice(0, 2).join('; ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function AgentChip({ opinion, active, onClick }) {
  const color = AGENT_COLORS[opinion.agent_id] || 'var(--accent)'
  const icon = AGENT_ICONS[opinion.agent_id] || '👤'
  return (
    <button onClick={onClick} style={{
      background: active ? `${color}22` : 'var(--surface2)',
      border: `1px solid ${active ? color : 'var(--border)'}`,
      color: active ? color : 'var(--text-muted)',
      borderRadius: 8, padding: '8px 14px', cursor: 'pointer',
      fontSize: 12, fontWeight: 500, display: 'flex', alignItems: 'center', gap: 6,
      transition: 'all 0.15s',
    }}>
      <span>{icon}</span>
      <span>{opinion.agent_name}</span>
    </button>
  )
}

function OpinionCard({ opinion, onClick }) {
  const color = AGENT_COLORS[opinion.agent_id] || 'var(--accent)'
  const icon = AGENT_ICONS[opinion.agent_id] || '👤'
  const preview = opinion.opinion.slice(0, 200).replace(/#+\s/g, '').replace(/\*\*/g, '') + '...'

  return (
    <div onClick={onClick} style={{
      background: 'var(--surface)', border: '1px solid var(--border)',
      borderRadius: 10, padding: 16, cursor: 'pointer',
      transition: 'border-color 0.15s, transform 0.1s',
      borderLeft: `3px solid ${color}`,
    }}
      onMouseEnter={e => e.currentTarget.style.borderColor = color}
      onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
        <span style={{ fontSize: 18 }}>{icon}</span>
        <div>
          <div style={{ fontWeight: 600, fontSize: 13, color }}>{opinion.agent_name}</div>
          <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{opinion.togaf_domain}</div>
        </div>
      </div>
      <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.6 }}>{preview}</p>
      <div style={{ marginTop: 10, fontSize: 11, color: color }}>Click to expand →</div>
    </div>
  )
}

function OpinionPanel({ opinion, reviews }) {
  const color = AGENT_COLORS[opinion.agent_id] || 'var(--accent)'
  const icon = AGENT_ICONS[opinion.agent_id] || '👤'
  const myReview = reviews.find(r => r.reviewer_id === opinion.agent_id)

  return (
    <div style={{ background: 'var(--surface)', border: `1px solid ${color}44`, borderRadius: 10, padding: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20, paddingBottom: 16, borderBottom: '1px solid var(--border)' }}>
        <span style={{ fontSize: 24 }}>{icon}</span>
        <div>
          <div style={{ fontWeight: 700, fontSize: 16, color }}>{opinion.agent_name}</div>
          <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{opinion.togaf_domain}</div>
        </div>
        <div style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--text-muted)', background: 'var(--surface2)', padding: '3px 8px', borderRadius: 4 }}>
          {opinion.model_used}
        </div>
      </div>
      <MarkdownWithMermaid content={opinion.opinion} />

      {myReview && myReview.gaps_identified.length > 0 && (
        <div style={{ marginTop: 20, padding: 16, background: 'var(--surface2)', borderRadius: 8 }}>
          <div style={{ fontWeight: 600, fontSize: 12, marginBottom: 8, color: 'var(--warning)' }}>
            🔍 This agent's identified gaps (from reviewing peers):
          </div>
          <ul style={{ margin: '0 0 0 16px', fontSize: 12, color: 'var(--text-muted)' }}>
            {myReview.gaps_identified.map((g, i) => <li key={i}>{g}</li>)}
          </ul>
        </div>
      )}
    </div>
  )
}

function ScoreBadge({ score }) {
  const color = score.total >= 80 ? '#34d399' : score.total >= 60 ? '#fbbf24' : '#f87171'
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>Initial Score:</div>
      <div style={{ background: `${color}22`, border: `1px solid ${color}`, color, borderRadius: 6, padding: '2px 10px', fontWeight: 700, fontSize: 14 }}>
        {score.total.toFixed(0)}/100
      </div>
    </div>
  )
}

function LoadingDots() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: 6, marginTop: 16 }}>
      {[0, 1, 2].map(i => (
        <div key={i} style={{
          width: 8, height: 8, borderRadius: '50%', background: 'var(--accent)',
          animation: `bounce 1.2s ${i * 0.2}s infinite`,
        }} />
      ))}
      <style>{`@keyframes bounce { 0%,80%,100% { transform: scale(0); } 40% { transform: scale(1); } }`}</style>
    </div>
  )
}

