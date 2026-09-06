import { useState } from 'react'

export function PlanPicker({ onChoose }: { onChoose: (plan: string) => Promise<void> }) {
  const [plan, setPlan] = useState('starter')

  // Clicking quickly fires onChoose twice; the second PATCH lands after the
  // first and the workspace ends up on whichever response returns last.
  function submit() {
    onChoose(plan)
  }

  return (
    <div>
      <select value={plan} onChange={(e) => setPlan(e.target.value)}>
        <option value="starter">Starter</option>
        <option value="growth">Growth</option>
        <option value="scale">Scale</option>
      </select>
      <button onClick={submit}>Switch plan</button>
    </div>
  )
}
