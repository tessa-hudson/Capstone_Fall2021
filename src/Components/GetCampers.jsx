import React, { Component } from 'react'
import { Button } from '@mui/material'
import '../Styles/GetCampers.css'

class GetCampers extends Component {
    constructor(props) {
        super(props)
        this.state = {Campers: ''}

        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        fetch('http://localhost:5000/attendees', {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        })
        .then(response => response.json())
        .then(data => {
        this.setState({campers: data.attendees});
        console.log('Success:', data.attendees);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    render() {
        return (
            <div className="GetCampers">
                <h3>Use this button to get the campers!</h3>
                <form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Campers!
                    </Button>
                </form>
                {
                  this.state.campers &&
                    this.state.campers.map((camper) => 
                        <h4 key={camper.id}>{camper.firstname} {camper.last_initial}</h4>
                    )
                }
            </div> 
        )
    }
}

export default GetCampers