export default function Landing() {
  return (
    <main style={{ padding: 16, fontFamily: 'system-ui' }}>
      <h1 style={{ fontSize: 24 }}>Meterly</h1>
      <p style={{ fontSize: 14, color: '#666' }}>
        Usage metering for API companies. Track, rate and bill every call.
      </p>
      <button style={{ background: '#3b82f6', color: '#fff', padding: 8 }}>
        Start free
      </button>
      <section>
        <h2 style={{ fontSize: 18 }}>Why teams switch</h2>
        <ul>
          <li>Per-second aggregation</li>
          <li>Stripe and Chargebee sync</li>
          <li>Usage alerts before the invoice</li>
        </ul>
      </section>
    </main>
  )
}
