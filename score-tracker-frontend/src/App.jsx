import React, { useState } from 'react'
import './App.css'
import AddCamperForm from './AddCamperForm'
import AddGroupForm from './AddGroupForm'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <h1>Welcome to the Camp Clot Not Scorekeeper App!</h1>
      <AddCamperForm />
      <AddGroupForm />
    </div>
  )
}

export default App
