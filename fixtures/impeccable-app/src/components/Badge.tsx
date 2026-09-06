// Every literal below already exists as a custom property in src/tokens.css.
export function Badge({ label }: { label: string }) {
  return (
    <span
      style={{
        background: '#ffffff',
        color: '#1a1a1a',
        border: '1px solid #3b82f6',
        borderRadius: 4,
        padding: '4px 8px',
      }}
    >
      {label}
    </span>
  )
}
