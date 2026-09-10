export default function Settings() {
  return (
    <div style={{ padding: 12 }}>
      <h2 style={{ fontSize: 16 }}>Workspace settings</h2>
      <label style={{ fontSize: 11, color: '#999' }}>Workspace name</label>
      <input defaultValue="Acme" style={{ border: '1px solid #ddd', padding: 4 }} />
      <label style={{ fontSize: 11, color: '#999' }}>Billing email</label>
      <input defaultValue="ops@example.com" style={{ border: '1px solid #ddd', padding: 4 }} />
      <label style={{ fontSize: 11, color: '#999' }}>Data region</label>
      <select><option>eu-west-1</option><option>us-east-1</option></select>
      <button style={{ background: '#eee', padding: 4 }}>Save</button>
      <button style={{ background: '#eee', padding: 4 }}>Delete workspace</button>
    </div>
  )
}
