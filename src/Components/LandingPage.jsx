import React, { Component } from 'react'
import AuthNav from './AuthNav'
import '../Styles/LandingPage.css'
import logo from '../HBDA/HBDA_LOGO_2017.png'

class LandingPage extends Component {
    render() {
        return (
            <div className="LandingPage">
                <h1>Welcome to HBDA Tracking Systems</h1>
                <AuthNav />
                <h4>For access, please speak to an administrator</h4>
                <img src={logo} alt="hbda" style={{width: "150px"}}/>
            </div>
        )
    }
}

export default LandingPage