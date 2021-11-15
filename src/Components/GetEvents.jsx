import React, { Component } from 'react'
import { Button, Grid } from '@mui/material'
import '../Styles/GetCampers.css'

class GetEvents extends Component {
    constructor(props) {
        super(props)
        this.state = {events: []}

        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteEvent = this.deleteEvent.bind(this)
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        fetch('https://hbda-tracking-backend.azurewebsites.net/events', {
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

    deleteEvent(event) {
        if (window.confirm(`Are you sure you want to delete ${event.event_name}`)) {
            const obj = {event_id: event.event_id}
            const json = JSON.stringify(obj)
            fetch('http://localhost:5000/events', {
                method: 'DELETE',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Accept': '*/*'
                },
                body: json,
                })
                .then(response => response.json())
                .then(data => {
                console.log('Success:', data);
                })
                .catch((error) => {
                console.error(error);
                });
            window.location.reload()
        } else {
            console.log("Delete prevented")
        }
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
                        <Grid>
                            <h4 key={event.id}>{event.event_name}</h4>
                            <Button onClick={() => {this.deleteEvent(event)}}>Delete</Button>
                        </Grid>
                        
                    )
                }
            </div> 
        )
    }
}

export default GetEvents