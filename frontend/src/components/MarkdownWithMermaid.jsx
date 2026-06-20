import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import MermaidDiagram from './MermaidDiagram'

export default function MarkdownWithMermaid({ content }) {
  if (!content) return null
  const parts = splitMermaid(content)
  return (
    <div>
      {parts.map((part, i) =>
        part.type === 'mermaid'
          ? (
            <div key={i}>
              <div style={{ fontSize: 11, color: 'var(--accent)', marginBottom: 4, fontWeight: 600, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                📊 Architecture Diagram
              </div>
              <MermaidDiagram chart={part.content} />
            </div>
          )
          : (
            <div key={i} className="markdown">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{part.content}</ReactMarkdown>
            </div>
          )
      )}
    </div>
  )
}

function splitMermaid(text) {
  const parts = []
  const regex = /```mermaid\r?\n([\s\S]*?)```/g
  let lastIndex = 0
  let match
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      const slice = text.slice(lastIndex, match.index)
      if (slice.trim()) parts.push({ type: 'text', content: slice })
    }
    parts.push({ type: 'mermaid', content: match[1].trim() })
    lastIndex = match.index + match[0].length
  }
  if (lastIndex < text.length) {
    const slice = text.slice(lastIndex)
    if (slice.trim()) parts.push({ type: 'text', content: slice })
  }
  return parts
}
