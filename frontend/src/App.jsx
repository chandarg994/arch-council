import { useState, useEffect, useCallback } from 'react'
import RequirementForm from './components/RequirementForm.jsx'
import CouncilView from './components/CouncilView.jsx'
import RatchetLog from './components/RatchetLog.jsx'
import FinalReport from './components/FinalReport.jsx'
import SessionList from './components/SessionList.jsx'

const API = '/api'

const STATUS_LABELS = {
  queued: { label: 'Queued', color: '#8892a4' },
  stage1_council: { label: '🏛️ Council: First Opinions', color: '#6c8cff' },
  stage2_review: { label: '🔍 Council: Cross-Review', color: '#a78bfa' },
  stage3_synthesis: { label: '⚗️ Chairman: Synthesizing Draft', color: '#fbbf24' },
  stage4_ratchet: { label: '🔄 Ratchet: Refining Solution', color: '#34d399' },
  stage5_finalizing: { label: '📝 Generating Final Report', color: '#6c8cff' },
  complete: { label: '✅ Complete', color: '#34d399' },
}

export default function App() {
  const [view, setView] = useState('new') // 'new' | 'session' | 'history'
  const [activeSessionId, setActiveSessionId] = useState(null)
  const [session, setSession] = useState(null)
  const [status, setStatus] = useState(null)
  const [activeTab, setActiveTab] = useState('council')
  const [polling, setPolling] = useState(false)

  // Poll status while pipeline running
  useEffect(() => {
    if (!activeSessionId || !polling) return

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API}/sessions/${activeSessionId}/status`)
        const s = await res.json()
        setStatus(s)

        // Fetch full session data periodically for live updates
        const fullRes = await fetch(`${API}/sessions/${activeSessionId}`)
        const full = await fullRes.json()
        setSession(full)

        // Stop polling when done or errored
        if (s.status === 'complete' || s.status.startsWith('error')) {
          setPolling(false)
        }
      } catch (e) {
        console.error('Poll error:', e)
      }
    }, 3000)

    return () => clearInterval(interval)
  }, [activeSessionId, polling])

  const handleSubmit = useCallback(async (formData) => {
    const res = await fetch(`${API}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })
    const { session_id } = await res.json()
    setActiveSessionId(session_id)
    setSession(null)
    setStatus({ status: 'queued', council_opinions_count: 0, ratchet_iterations: 0 })
    setPolling(true)
    setView('session')
    setActiveTab('council')
  }, [])

  const handleSelectSession = useCallback(async (id) => {
    const res = await fetch(`${API}/sessions/${id}`)
    const full = await res.json()
    setSession(full)
    setActiveSessionId(id)
    setStatus({
      status: full.status,
      council_opinions_count: full.council_opinions?.length || 0,
      ratchet_iterations: full.ratchet_iterations?.length || 0,
      best_score: full.best_score?.total,
      final_report_ready: !!full.final_report,
    })
    if (!['complete', 'error'].some(x => full.status === x || full.status.startsWith('error'))) {
      setPolling(true)
    }
    setView('session')
    setActiveTab(full.final_report ? 'report' : 'council')
  }, [])

  const statusInfo = status ? (STATUS_LABELS[status.status] || { label: status.status, color: '#8892a4' }) : null

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Header */}
      <header style={{
        background: 'var(--surface)', borderBottom: '1px solid var(--border)',
        padding: '0 24px', display: 'flex', alignItems: 'center', gap: 16, height: 56,
      }}>
        <span style={{ fontSize: 20 }}>🏛️</span>
        <span style={{ fontWeight: 700, fontSize: 16, letterSpacing: '-0.3px' }}>ARCH-COUNCIL</span>
        <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>
          Multi-Agent AI Solutions Architecture · TOGAF-Aligned
        </span>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
          <NavBtn active={view === 'new'} onClick={() => setView('new')}>+ New</NavBtn>
          <NavBtn active={view === 'history'} onClick={() => setView('history')}>History</NavBtn>
          {view === 'session' && activeSessionId && (
            <NavBtn active={true} onClick={() => {}}>Session</NavBtn>
          )}
        </div>
      </header>

      {/* Main */}
      <main style={{ flex: 1, padding: 24, maxWidth: 1400, margin: '0 auto', width: '100%' }}>

        {view === 'new' && (
          <RequirementForm onSubmit={handleSubmit} />
        )}

        {view === 'history' && (
          <SessionList onSelect={handleSelectSession} />
        )}

        {view === 'session' && (
          <div>
            {/* Status Banner */}
            {statusInfo && (
              <div style={{
                background: 'var(--surface)', border: `1px solid ${statusInfo.color}33`,
                borderRadius: 10, padding: '12px 20px', marginBottom: 20,
                display: 'flex', alignItems: 'center', gap: 16,
              }}>
                <div style={{
                  width: 10, height: 10, borderRadius: '50%',
                  background: statusInfo.color,
                  boxShadow: status?.status !== 'complete' && !status?.status.startsWith('error')
                    ? `0 0 8px ${statusInfo.color}` : 'none',
                  animation: polling ? 'pulse 1.5s infinite' : 'none',
                }} />
                <span style={{ color: statusInfo.color, fontWeight: 600 }}>{statusInfo.label}</span>
                {status && (
                  <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>
                    {status.council_opinions_count > 0 && `${status.council_opinions_count}/6 opinions`}
                    {status.ratchet_iterations > 0 && ` · ${status.ratchet_iterations} ratchet iterations`}
                    {status.best_score != null && ` · Score: ${status.best_score.toFixed(1)}/100`}
                  </span>
                )}
              </div>
            )}

            {/* Tabs */}
            <div style={{ display: 'flex', gap: 4, marginBottom: 20, borderBottom: '1px solid var(--border)', paddingBottom: 0 }}>
              {[
                { id: 'council', label: '🏛️ Council Opinions', show: true },
                { id: 'ratchet', label: '🔄 Ratchet Log', show: (status?.ratchet_iterations || 0) > 0 },
                { id: 'report', label: '📄 Final Report', show: status?.final_report_ready },
              ].filter(t => t.show).map(t => (
                <Tab key={t.id} active={activeTab === t.id} onClick={() => setActiveTab(t.id)}>
                  {t.label}
                </Tab>
              ))}
            </div>

            {activeTab === 'council' && (
              <CouncilView
                opinions={session?.council_opinions || []}
                reviews={session?.cross_reviews || []}
                initialDraft={session?.initial_draft}
                initialScore={session?.initial_score}
                loading={polling && (session?.council_opinions?.length || 0) === 0}
              />
            )}

            {activeTab === 'ratchet' && (
              <RatchetLog
                iterations={session?.ratchet_iterations || []}
                bestScore={session?.best_score}
                loading={polling && status?.status === 'stage4_ratchet' && (session?.ratchet_iterations?.length || 0) === 0}
              />
            )}

            {activeTab === 'report' && (
              <FinalReport
                report={session?.final_report}
                score={session?.best_score}
                requirement={session?.requirement}
              />
            )}
          </div>
        )}
      </main>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </div>
  )
}

function NavBtn({ active, onClick, children }) {
  return (
    <button onClick={onClick} style={{
      background: active ? 'var(--accent)22' : 'transparent',
      border: `1px solid ${active ? 'var(--accent)' : 'var(--border)'}`,
      color: active ? 'var(--accent)' : 'var(--text-muted)',
      borderRadius: 6, padding: '4px 14px', cursor: 'pointer', fontSize: 13, fontWeight: 500,
      transition: 'all 0.15s',
    }}>{children}</button>
  )
}

function Tab({ active, onClick, children }) {
  return (
    <button onClick={onClick} style={{
      background: 'transparent', border: 'none',
      borderBottom: active ? '2px solid var(--accent)' : '2px solid transparent',
      color: active ? 'var(--accent)' : 'var(--text-muted)',
      padding: '8px 16px', cursor: 'pointer', fontSize: 13, fontWeight: 500,
      marginBottom: -1, transition: 'all 0.15s',
    }}>{children}</button>
  )
}
