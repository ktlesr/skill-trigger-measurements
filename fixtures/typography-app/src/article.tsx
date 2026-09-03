export function Article({ body }: { body: string }) {
  return (
    <article style={{ width: 1400 }}>
      <h2 className="section-head">Why measurement beats intuition</h2>
      <p className="body">{body}</p>
    </article>
  )
}
