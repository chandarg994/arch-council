import { useState } from 'react'
import MarkdownWithMermaid from './MarkdownWithMermaid'

export default function FinalReport({ report, score, requirement }) {
  const [copied, setCopied] = useState(false)

  if (!report) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div style={{ fontSize: 32, marginBottom: 16 }}>📝</div>
        <div style={{ color: 'var(--text-muted)' }}>Final report not yet available.</div>
      </div>
    )
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(report)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = () => {
    const blob = new Blob([report], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `arch-council-report-${Date.now()}.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div>
      {/* Report Header */}
      <div style={{
        background: 'var(--surface)', border: '1px solid var(--border)',
        borderRadius: 10, padding: '16px 20px', marginBottom: 20,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div>
          <div style={{ fontWeight: 700, fontSize: 16 }}>📄 Final Architecture Report</div>
          {requirement && (
            <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
              {requirement.industry} · Refined by ARCH-COUNCIL
            </div>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {score && <QualityBadge score={score} />}
          <button onClick={handleCopy} style={btnStyle}>
            {copied ? '✅ Copied' : '📋 Copy'}
          </button>
          <button onClick={handleDownload} style={{ ...btnStyle, background: 'var(--accent)22', borderColor: 'var(--accent)', color: 'var(--accent)' }}>
            ⬇️ Download .md
          </button>
        </div>
      </div>

      {/* Report Content */}
      <div style={{
        background: 'var(--surface)', border: '1px solid var(--border)',
        borderRadius: 10, padding: '28px 32px',
      }}>
        <MarkdownWithMermaid content={report} />
      </div>
    </div>
  )
}

function QualityBadge({ score }) {
  const total = score.total
  const color = total >= 80 ? '#34d399' : total >= 60 ? '#fbbf24' : '#f87171'
  const label = total >= 80 ? 'High Quality' : total >= 60 ? 'Good' : 'Needs Review'
  return (
    <div style={{
      background: `${color}15`, border: `1px solid ${color}44`,
      borderRadius: 8, padding: '6px 14px', textAlign: 'center',
    }}>
      <div style={{ fontSize: 18, fontWeight: 700, color }}>{total.toFixed(0)}<span style={{ fontSize: 12 }}>/100</span></div>
      <div style={{ fontSize: 10, color, marginTop: 1 }}>{label}</div>
    </div>
  )
}

const btnStyle = {
  background: 'var(--surface2)', border: '1px solid var(--border)',
  color: 'var(--text-muted)', borderRadius: 6, padding: '6px 14px',
  cursor: 'pointer', fontSize: 12, fontWeight: 500,
}

