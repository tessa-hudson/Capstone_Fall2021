import React, { useState } from 'react'
import { Route, Switch, NavLink} from "react-router-dom"
import './App.css'
import AddCamperForm from './Components/Forms/AddCamperForm'
import AddGroupForm from './Components/Forms/AddGroupForm'
import HomePage from './Components/HomePage'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <nav className="App-nav">
        <NavLink exact activeClassName="active-link" to="/">Home</NavLink>
        <NavLink exact activeClassName="active-link" to="addCamper">Add Camper</NavLink>
        <NavLink exact activeClassName="active-link" to="addGroup">Add Group</NavLink>
      </nav>
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route exact path="/addCamper" component={AddCamperForm} />
        <Route exact path="/addGroup" component={AddGroupForm} />
      </Switch>
    </div>
  )
}

export default App
