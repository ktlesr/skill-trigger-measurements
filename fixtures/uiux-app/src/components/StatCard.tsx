export function StatCard({ label, value, delta }: { label: string; value: string; delta: number }) {
  return (
    <div style={{ padding: 8, background: '#fff', border: '1px solid #eee' }}>
      <span style={{ fontSize: 11, color: '#aaa' }}>{label}</span>
      <span style={{ fontSize: 13, color: '#222' }}>{value}</span>
      <span style={{ fontSize: 11, color: delta >= 0 ? '#7ac142' : '#e04b4b' }}>
        {delta >= 0 ? '▲' : '▼'} {Math.abs(delta)}%
      </span>
      <div onClick={() => console.log('drill in')}>⋯</div>
    </div>
  )
}
