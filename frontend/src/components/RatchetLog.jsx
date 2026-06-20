export default function RatchetLog({ iterations, bestScore, loading }) {
  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div style={{ fontSize: 32, marginBottom: 16 }}>🔄</div>
        <div style={{ color: 'var(--success)', fontWeight: 600 }}>Ratchet loop running...</div>
        <div style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 8 }}>
          Agents are proposing and evaluating improvements one by one
        </div>
      </div>
    )
  }

  if (iterations.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
        Ratchet not started yet.
      </div>
    )
  }

  const accepted = iterations.filter(it => it.accepted)
  const rejected = iterations.filter(it => !it.accepted)
  const scores = iterations.map(it => it.score_after)
  const minScore = Math.min(...scores)
  const maxScore = Math.max(...scores)

  return (
    <div>
      {/* Summary Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 20 }}>
        <StatCard label="Total Iterations" value={iterations.length} color="var(--accent)" />
        <StatCard label="Accepted" value={accepted.length} color="var(--success)" />
        <StatCard label="Rejected" value={rejected.length} color="var(--danger)" />
        <StatCard label="Best Score" value={bestScore ? `${bestScore.total.toFixed(1)}/100` : '—'} color="var(--warning)" />
      </div>

      {/* Score Progression Chart (ASCII sparkline) */}
      {iterations.length > 1 && (
        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: 16, marginBottom: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 12 }}>📈 Score Progression</div>
          <ScoreChart iterations={iterations} />
        </div>
      )}

      {/* Score Breakdown */}
      {bestScore && (
        <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: 16, marginBottom: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 12 }}>🎯 Current Best Score Breakdown</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
            <ScoreDim label="TOGAF Compliance" value={bestScore.togaf_compliance} max={25} color="var(--accent)" />
            <ScoreDim label="Technical Feasibility" value={bestScore.technical_feasibility} max={25} color="var(--success)" />
            <ScoreDim label="Business Alignment" value={bestScore.business_alignment} max={25} color="var(--warning)" />
            <ScoreDim label="Risk & Governance" value={bestScore.risk_governance} max={25} color="var(--danger)" />
          </div>
          {bestScore.reasoning && (
            <div style={{ marginTop: 12, fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>
              "{bestScore.reasoning}"
            </div>
          )}
        </div>
      )}

      {/* Iteration Log */}
      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, overflow: 'hidden' }}>
        <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)', fontWeight: 600, fontSize: 13 }}>
          📋 Iteration Log
        </div>
        <div style={{ maxHeight: 480, overflowY: 'auto' }}>
          {[...iterations].reverse().map(it => (
            <IterationRow key={it.iteration} it={it} />
          ))}
        </div>
      </div>
    </div>
  )
}

function IterationRow({ it }) {
  const accepted = it.accepted && !it.proposed_improvement.startsWith('[ERROR')
  const isError = it.proposed_improvement.startsWith('[ERROR')
  const delta = it.delta

  return (
    <div style={{
      display: 'flex', alignItems: 'flex-start', gap: 12, padding: '10px 16px',
      borderBottom: '1px solid var(--border)',
      background: isError ? '#f8717108' : accepted ? '#34d39908' : 'transparent',
    }}>
      {/* Iteration number */}
      <div style={{ width: 28, flexShrink: 0, textAlign: 'right', color: 'var(--text-muted)', fontSize: 12, paddingTop: 2 }}>
        #{it.iteration}
      </div>

      {/* Status icon */}
      <div style={{ fontSize: 14, flexShrink: 0, paddingTop: 1 }}>
        {isError ? '❌' : accepted ? '✅' : '↩️'}
      </div>

      {/* Content */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 12, fontWeight: 500, marginBottom: 2 }}>
          <span style={{ color: 'var(--text-muted)' }}>{it.proposing_agent_name}:</span>{' '}
          <span>{it.proposed_improvement}</span>
        </div>
        {it.reasoning && (
          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2, fontStyle: 'italic' }}>
            {it.reasoning}
          </div>
        )}
      </div>

      {/* Score delta */}
      <div style={{ flexShrink: 0, textAlign: 'right' }}>
        <div style={{ fontSize: 12, fontWeight: 600, color: delta > 0 ? 'var(--success)' : delta < 0 ? 'var(--danger)' : 'var(--text-muted)' }}>
          {delta > 0 ? `+${delta.toFixed(1)}` : delta.toFixed(1)}
        </div>
        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{it.score_after.toFixed(1)}</div>
      </div>
    </div>
  )
}

function ScoreChart({ iterations }) {
  const scores = iterations.map(it => it.score_after)
  const min = Math.min(...scores) - 2
  const max = Math.max(...scores) + 2
  const W = 600, H = 80

  const points = scores.map((s, i) => {
    const x = (i / (scores.length - 1)) * W
    const y = H - ((s - min) / (max - min)) * H
    return `${x},${y}`
  }).join(' ')

  return (
    <div style={{ overflowX: 'auto' }}>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 80 }}>
        <polyline points={points} fill="none" stroke="var(--success)" strokeWidth="2" />
        {scores.map((s, i) => {
          const x = (i / (scores.length - 1)) * W
          const y = H - ((s - min) / (max - min)) * H
          const it = iterations[i]
          return (
            <circle key={i} cx={x} cy={y} r={3}
              fill={it.accepted ? 'var(--success)' : 'var(--surface2)'}
              stroke={it.accepted ? 'var(--success)' : 'var(--border)'}
              strokeWidth={1}
            />
          )
        })}
      </svg>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>
        <span>Iteration 1</span>
        <span>Iteration {iterations.length}</span>
      </div>
    </div>
  )
}

function StatCard({ label, value, color }) {
  return (
    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: '14px 16px' }}>
      <div style={{ fontSize: 22, fontWeight: 700, color }}>{value}</div>
      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>{label}</div>
    </div>
  )
}

function ScoreDim({ label, value, max, color }) {
  const pct = (value / max) * 100
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{label}</span>
        <span style={{ fontSize: 12, fontWeight: 600, color }}>{value}/{max}</span>
      </div>
      <div style={{ height: 4, background: 'var(--surface2)', borderRadius: 2 }}>
        <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: 2, transition: 'width 0.5s' }} />
      </div>
    </div>
  )
}
