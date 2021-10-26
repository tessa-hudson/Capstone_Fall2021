import React, { Component } from 'react'
import { Button } from '@mui/material'
import '../Styles/GetCampers.css'

class GetEvents extends Component {
    constructor(props) {
        super(props)
        this.state = {events: []}

        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        fetch('https://hbdatracking-backend.azurewebsites.net/events', {
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
        this.setState({events: data.events});
        console.log('Success:', data.events);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    render() {
        return (
            <div className="GetCampers">
                <h3>Use this button to get the events!</h3>
                <form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Events!
                    </Button>
                </form>
                {
                  this.state.events &&
                    this.state.events.map((event) => 
                        <h4 key={event.id}>{event.event_name}</h4>
                    )
                }
            </div> 
        )
    }
}

export default GetEvents