import React, { Component } from 'react'
import '../Styles/HomePage.css'
import Scoreboard from './Scoreboard'

class HomePage extends Component {
    render() {
        return (
            <div className="Home">
                <h1>Welcome to the Camp Clot Not Score Keeper!</h1>
                <h3>See the ScoreBoard Below!</h3>
                <Scoreboard />
            </div>
            
        )
    }
}

export default HomePage