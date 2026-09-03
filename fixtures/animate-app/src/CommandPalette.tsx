import './palette.css'

// Opened with Cmd+K, many times a day.
export function CommandPalette({ open }: { open: boolean }) {
  return <div className={open ? 'palette palette--open' : 'palette'} />
}
