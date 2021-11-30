import React, { Component } from 'react'
import AuthNav from './AuthNav'
import { NavLink } from "react-router-dom"
import logo from '../HBDA/HBDA_LOGO-2017-No_Words.jpg'

class NavBar extends Component {
    render() {
        return (
            <div className="Nav">
                <div>
                    <img src={logo} alt="logo"/>
                </div>
                { window.location.pathname !== '/' &&
                    <nav className="App-nav">
                        <NavLink exact activeClassName="active-link" to="/home">Home</NavLink>
                        <NavLink exact activeClassName="active-link" to="/groups">Groups</NavLink>
                        <NavLink exact activeClassName="active-link" to="/attendees">Attendees</NavLink>
                        <NavLink exact activeClassName="active-link" to="/events">Events</NavLink>
                        <AuthNav />
                    </nav>
                }
            </div>
        )
    }
}

export default NavBar