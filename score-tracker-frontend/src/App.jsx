import React, { useState } from 'react'
import { Route, Switch, NavLink} from "react-router-dom"
import './App.css'
import AddCamperForm from './Components/Forms/AddCamperForm'
import AddGroupForm from './Components/Forms/AddGroupForm'
import HomePage from './Components/HomePage'
import Groups from './Components/Groups.jsx'
import Campers from './Components/Campers.jsx'

function App() {
  return (
    <div className="App">
      <div className="Nav">
        <nav className="App-nav">
          <NavLink exact activeClassName="active-link" to="/">Home</NavLink>
          <NavLink exact activeClassName="active-link" to="/groups">Groups</NavLink>
          <NavLink exact activeClassName="active-link" to="/campers">Campers</NavLink>
        </nav>
      </div>
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route exact path="/groups" component={Groups} />
        <Route exact path="/campers" component={Campers} />
      </Switch>
    </div>
  )
}

export default App
