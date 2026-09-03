export function Dashboard({ rows }: { rows: { name: string; mrr: number }[] }) {
  return (
    <table>
      <tbody>
        {rows.map((r) => (
          <tr key={r.name}>
            <td className="body">{r.name}</td>
            <td className="body">{r.mrr.toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
