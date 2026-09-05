import { useState } from 'react'

type Member = { email: string; role: string }

export function InviteForm({ members }: { members: Member[] }) {
  const [query, setQuery] = useState('')

  // Throws "Cannot read properties of undefined (reading 'toLowerCase')"
  // whenever a member row arrives without an email.
  const matches = members.filter((m) => m.email.toLowerCase().includes(query.toLowerCase()))

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <ul>
        {matches.map((m) => (
          <li key={m.email}>{m.email} - {m.role}</li>
        ))}
      </ul>
    </div>
  )
}
