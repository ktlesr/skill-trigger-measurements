import './modal.css'

export function Modal({ open, children }: { open: boolean; children: React.ReactNode }) {
  if (!open) return null
  return (
    <div className="overlay">
      <div className="modal">{children}</div>
    </div>
  )
}
