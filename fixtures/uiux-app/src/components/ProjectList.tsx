import { useEffect, useState } from 'react'

export function ProjectList({ orgId }: { orgId: string }) {
  const [projects, setProjects] = useState<{ id: string; name: string }[]>([])
  const [filters] = useState({ archived: false })

  // Refetches on every render: `filters` is a fresh object each time.
  useEffect(() => {
    fetch(`/api/projects?org=${orgId}`)
      .then((r) => r.json())
      .then(setProjects)
  })

  return (
    <ul>
      {projects.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  )
}
