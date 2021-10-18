import React, { Component } from 'react'
import AuthNav from './AuthNav'
import Scoreboard from './Scoreboard'

class LandingPage extends Component {
    render() {
        return (
            <div className="LandingPage">
                <h1>Welcome to the Camp Clot Not Score Keeper!</h1>
                <AuthNav />
            </div>
            
        )
    }
}

export default LandingPage