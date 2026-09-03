export function Toast({ message, visible }: { message: string; visible: boolean }) {
  if (!visible) return null
  return <div className="toast">{message}</div>
}
