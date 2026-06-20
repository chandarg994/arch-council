import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

let initialized = false

function ensureInit() {
  if (!initialized) {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'dark',
      themeVariables: {
        primaryColor: '#1e293b',
        primaryBorderColor: '#6c8cff',
        primaryTextColor: '#f1f5f9',
        lineColor: '#6c8cff',
        secondaryColor: '#0f172a',
        tertiaryColor: '#1e293b',
        fontSize: '13px',
      },
      flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
    })
    initialized = true
  }
}

export default function MermaidDiagram({ chart }) {
  const [svg, setSvg] = useState('')
  const [error, setError] = useState(null)
  const idRef = useRef(`mmd-${Math.random().toString(36).slice(2)}`)

  useEffect(() => {
    ensureInit()
    let cancelled = false
    async function render() {
      try {
        const { svg: rendered } = await mermaid.render(idRef.current, chart)
        if (!cancelled) setSvg(rendered)
      } catch (e) {
        if (!cancelled) setError(e.message || 'Render failed')
      }
    }
    render()
    return () => { cancelled = true }
  }, [chart])

  if (error) {
    return (
      <div style={{ background: '#1c1030', border: '1px dashed #f8717166', borderRadius: 8, padding: '12px 16px', margin: '12px 0' }}>
        <div style={{ fontSize: 11, color: '#f87171', marginBottom: 6 }}>Diagram parse error — raw source:</div>
        <pre style={{ margin: 0, fontSize: 10, color: '#94a3b8', whiteSpace: 'pre-wrap' }}>{chart}</pre>
      </div>
    )
  }

  if (!svg) {
    return (
      <div style={{ background: 'var(--surface2)', borderRadius: 8, padding: 20, textAlign: 'center', color: 'var(--text-muted)', fontSize: 12, margin: '12px 0' }}>
        Rendering diagram...
      </div>
    )
  }

  return (
    <div style={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8, padding: 16, margin: '12px 0', overflow: 'auto', textAlign: 'center' }}>
      <div dangerouslySetInnerHTML={{ __html: svg }} />
    </div>
  )
}
