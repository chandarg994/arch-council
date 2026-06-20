import { useState } from 'react'

const INDUSTRIES = [
  'Financial Services', 'Healthcare', 'Retail & E-Commerce', 'Manufacturing',
  'Logistics & Supply Chain', 'Telecommunications', 'Education', 'Government & Public Sector',
  'Energy & Utilities', 'Media & Entertainment', 'Professional Services', 'Other',
]

const EXAMPLE = {
  industry: 'Financial Services',
  client_context: 'Mid-sized regional bank with 500k retail customers. Currently processes loan applications manually — each application takes 3-5 business days. Has core banking on Oracle, CRM on Salesforce, and document storage in SharePoint.',
  pain_points: 'Loan application processing is too slow (3-5 days vs fintech competitors at <24 hours). High manual effort from credit analysts reviewing documents. Inconsistent decisions due to analyst subjectivity. Cannot scale without hiring more analysts.',
  constraints: 'Budget: $500k for Year 1 implementation. Must comply with RBI/GDPR regulations. No access to customer PII in cloud (data sovereignty). Must integrate with existing Oracle core banking. Go-live target: 6 months.',
  existing_systems: 'Oracle Core Banking (on-prem), Salesforce CRM (cloud), SharePoint Online (document storage), Python/SQL data team, no existing ML infrastructure.',
}

export default function RequirementForm({ onSubmit }) {
  const [form, setForm] = useState({
    industry: '',
    client_context: '',
    pain_points: '',
    constraints: '',
    existing_systems: '',
  })
  const [loading, setLoading] = useState(false)

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await onSubmit(form)
    } finally {
      setLoading(false)
    }
  }

  const loadExample = () => setForm(EXAMPLE)

  const isValid = Object.values(form).every(v => v.trim().length > 0)

  return (
    <div style={{ maxWidth: 760, margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
          🏛️ ARCH-COUNCIL
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: 15 }}>
          6 specialized TOGAF architects + overnight ratchet refinement → production-grade AI solution architecture
        </p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: 24, marginTop: 16 }}>
          {['Business Architect', 'Data Architect', 'App Architect', 'Tech Architect', 'AI/ML Specialist', 'Risk Reviewer'].map(a => (
            <span key={a} style={{ fontSize: 11, color: 'var(--text-muted)', background: 'var(--surface2)', padding: '3px 8px', borderRadius: 4 }}>{a}</span>
          ))}
        </div>
      </div>

      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12, padding: 28 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <h2 style={{ fontSize: 16, fontWeight: 600 }}>Client Requirement</h2>
          <button onClick={loadExample} style={{
            background: 'var(--surface2)', border: '1px solid var(--border)',
            color: 'var(--text-muted)', borderRadius: 6, padding: '4px 12px',
            cursor: 'pointer', fontSize: 12,
          }}>Load Example</button>
        </div>

        <form onSubmit={handleSubmit}>
          <Field label="Industry" required>
            <select value={form.industry} onChange={set('industry')} style={inputStyle}>
              <option value="">Select industry...</option>
              {INDUSTRIES.map(i => <option key={i} value={i}>{i}</option>)}
            </select>
          </Field>

          <Field label="Client Context" hint="Who is the client? What do they do? What's their current situation?" required>
            <textarea value={form.client_context} onChange={set('client_context')}
              placeholder="e.g. Mid-sized logistics company, 200 employees, currently manages fleet of 500 trucks manually..."
              rows={4} style={inputStyle} />
          </Field>

          <Field label="Pain Points" hint="What specific problems need solving? Be concrete." required>
            <textarea value={form.pain_points} onChange={set('pain_points')}
              placeholder="e.g. Route optimization takes 2 hours manually each morning, driver allocation is inefficient, fuel costs 20% above benchmark..."
              rows={4} style={inputStyle} />
          </Field>

          <Field label="Constraints" hint="Budget, timeline, regulatory, technical constraints." required>
            <textarea value={form.constraints} onChange={set('constraints')}
              placeholder="e.g. Budget: $200k Year 1, GDPR compliance required, must not replace existing ERP, go-live in 4 months..."
              rows={3} style={inputStyle} />
          </Field>

          <Field label="Existing Systems" hint="Current tech stack, tools, and infrastructure in place." required>
            <textarea value={form.existing_systems} onChange={set('existing_systems')}
              placeholder="e.g. SAP S/4HANA (ERP), Salesforce (CRM), Azure cloud account, small Python data team, no ML experience..."
              rows={3} style={inputStyle} />
          </Field>

          <button
            type="submit"
            disabled={!isValid || loading}
            style={{
              width: '100%', padding: '12px 24px', marginTop: 8,
              background: isValid && !loading ? 'var(--accent)' : 'var(--surface2)',
              color: isValid && !loading ? 'white' : 'var(--text-muted)',
              border: 'none', borderRadius: 8, fontSize: 15, fontWeight: 600,
              cursor: isValid && !loading ? 'pointer' : 'not-allowed',
              transition: 'all 0.15s',
            }}
          >
            {loading ? '⏳ Submitting...' : '🚀 Launch Architecture Council'}
          </button>
        </form>
      </div>

      <div style={{ marginTop: 20, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 10, padding: '16px 20px' }}>
        <div style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.8 }}>
          <strong style={{ color: 'var(--text)' }}>What happens next:</strong>
          <span style={{ marginLeft: 8 }}>
            Stage 1 → 6 agents analyze in parallel (5–10 min) →
            Stage 2 → Cross-review (3–5 min) →
            Stage 3 → Chairman synthesizes draft (2–3 min) →
            Stage 4 → Ratchet refinement loop (20 iterations) →
            Stage 5 → Final architecture document
          </span>
        </div>
      </div>
    </div>
  )
}

function Field({ label, hint, required, children }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <label style={{ display: 'block', marginBottom: 6, fontWeight: 500, fontSize: 13 }}>
        {label} {required && <span style={{ color: 'var(--danger)' }}>*</span>}
        {hint && <span style={{ color: 'var(--text-muted)', fontWeight: 400, marginLeft: 8 }}>{hint}</span>}
      </label>
      {children}
    </div>
  )
}

const inputStyle = {
  width: '100%', background: 'var(--surface2)', border: '1px solid var(--border)',
  borderRadius: 8, padding: '10px 14px', color: 'var(--text)', fontSize: 13,
  fontFamily: 'inherit', resize: 'vertical', outline: 'none',
  transition: 'border-color 0.15s',
}
