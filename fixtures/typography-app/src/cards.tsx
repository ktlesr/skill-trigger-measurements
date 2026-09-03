export function Cards({ items }: { items: string[] }) {
  return (
    <div className="card-grid">
      {items.map((i) => (
        <div className="card" key={i}>
          <h2 className="card-title">{i}</h2>
          <p className="caption-muted">Updated recently</p>
        </div>
      ))}
    </div>
  )
}
