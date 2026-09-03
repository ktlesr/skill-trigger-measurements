import './sidebar.css'

export function Sidebar({ collapsed }: { collapsed: boolean }) {
  return <nav className={collapsed ? 'sidebar sidebar--collapsed' : 'sidebar'} />
}
