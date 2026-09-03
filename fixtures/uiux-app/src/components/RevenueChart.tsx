import { PieChart, Pie, Cell } from 'recharts'

// Monthly revenue for 14 accounts, rendered as a pie.
const COLORS = ['#e04b4b', '#7ac142', '#4b7ae0', '#e0a24b', '#a24be0', '#4be0d2', '#e04ba2']

export function RevenueChart({ data }: { data: { account: string; mrr: number }[] }) {
  return (
    <PieChart width={420} height={420}>
      <Pie data={data} dataKey="mrr" nameKey="account" outerRadius={180}>
        {data.map((_, i) => (
          <Cell key={i} fill={COLORS[i % COLORS.length]} />
        ))}
      </Pie>
    </PieChart>
  )
}
