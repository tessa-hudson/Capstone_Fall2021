import React, { Component } from 'react'
import AuthNav from './AuthNav'
import { Route, Switch, NavLink} from "react-router-dom"

class NavBar extends Component {
    render() {
        return (
            <div className="Nav">
                <nav className="App-nav">
                    <NavLink exact activeClassName="active-link" to="/home">Home</NavLink>
                    <NavLink exact activeClassName="active-link" to="/groups">Groups</NavLink>
                    <NavLink exact activeClassName="active-link" to="/campers">Campers</NavLink>
                    <AuthNav />
                </nav>
            </div>
        )
    }
}

export default NavBar