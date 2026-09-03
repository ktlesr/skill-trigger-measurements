export type Product = { id: string; title: string; price: number }

export function listProducts(rows: Product[]) {
  // titles come back from the vendor feed at up to 300 characters
  return rows.map((r) => ({ id: r.id, title: r.title, price: r.price }))
}
