import { useState } from 'react'

export default function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [link, setLink] = useState('')
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLink('')
    const res = await fetch('/api/invite', {
      method: 'POST',
      body: new URLSearchParams({ username, password }),
    })
    if (!res.ok) {
      alert('Login failed')
      return
    }
    const data = await res.json()
    setLink(data.link)
  }
  return (
    <div>
      <h1>n8n Invite</h1>
      <form onSubmit={submit}>
        <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
      {link && <p>Invite link: <a href={link}>{link}</a></p>}
    </div>
  )
}
