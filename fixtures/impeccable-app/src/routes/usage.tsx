type Row = { customer: string; calls: number; overage: number }

export default function Usage({ rows }: { rows: Row[] }) {
  return (
    <div style={{ padding: 12, fontFamily: 'system-ui' }}>
      <h2 style={{ fontSize: 16 }}>Usage this month</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
        <div style={{ border: '1px solid #ddd', padding: 8 }}>
          <div style={{ fontSize: 11, color: '#999' }}>Calls</div>
          <div style={{ fontSize: 18 }}>{rows.reduce((n, r) => n + r.calls, 0)}</div>
        </div>
        <div style={{ border: '1px solid #ddd', padding: 8 }}>
          <div style={{ fontSize: 11, color: '#999' }}>Overage</div>
          <div style={{ fontSize: 18 }}>{rows.reduce((n, r) => n + r.overage, 0)}</div>
        </div>
        <div style={{ border: '1px solid #ddd', padding: 8 }}>
          <div style={{ fontSize: 11, color: '#999' }}>Customers</div>
          <div style={{ fontSize: 18 }}>{rows.length}</div>
        </div>
      </div>
      <table>
        <tbody>
          {rows.map((r) => (
            <tr key={r.customer}>
              <td style={{ fontSize: 12 }}>{r.customer}</td>
              <td style={{ fontSize: 12 }}>{r.calls}</td>
              <td style={{ fontSize: 12 }}>{r.overage}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
