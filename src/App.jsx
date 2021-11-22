import React from 'react'
import { Route, Switch} from "react-router-dom"
import './App.css'
import './index.css'
import HomePage from './Components/HomePage'
import Groups from './Components/Groups'
import Attendees from './Components/Attendees'
import Events from './Components/Events'
import Profile from './Components/Profile'
import LandingPage from './Components/LandingPage'
import ProtectedRoute from './auth/ProtectedRoute'
import NavBar from './Components/NavBar'
import GroupUpdateForm from './Components/Forms/GroupUpdateForm'
import AttendeeUpdateForm from './Components/Forms/AttendeeUpdateForm'
import EventUpdateForm from './Components/Forms/EventUpdateForm'

function App() {
  return (
    <div className="App">
      {
        window.location.pathname !== '/' && <NavBar />
      }
      <Switch>
        <Route exact path="/" component={LandingPage} />
        <ProtectedRoute exact path="/home" component={HomePage} />
        <ProtectedRoute exact path="/groups" component={Groups} />
        <ProtectedRoute exact path="/attendees" component={Attendees} />
        <ProtectedRoute exact path="/events" component ={Events} />
        <ProtectedRoute exact path="/profile" component={Profile} />
        <ProtectedRoute exact path="/update/groups" component={GroupUpdateForm} />
        <ProtectedRoute exact path="/update/events" component={EventUpdateForm} />
        <ProtectedRoute exact path="/update/attendees" component={AttendeeUpdateForm} />
      </Switch>
    </div>
  );
}

export default App;
