import React, { useState } from 'react'
import { Button, Grid } from '@mui/material'
import { Link } from "react-router-dom"
import '../Styles/GetAttendees.css'
<<<<<<< HEAD
=======
import { useAuth0 } from '@auth0/auth0-react'
>>>>>>> f3f95f88def85be96afb9511bd6e6300f7903154

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function GetEvents (props) {
    const [events, setEvents] = useState([])
    const {getAccessTokenSilently} = useAuth0() 

    const handleSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit

        getAccessTokenSilently()
        .then((accessToken) =>
            fetch(`${request_url}/events`, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*',
            'Authorization': `Bearer ${accessToken}`
        },
        }))
        .then(response => response.json())
        .then(data => {
        setEvents(data.events);
        console.log('Success:', data.events);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    const deleteEvent = (event) => {
        if (window.confirm(`Are you sure you want to delete ${event.event_name}`)) {
            getAccessTokenSilently()
            .then((accessToken) => fetch(`${request_url}/events/${event.event_id}`, {
                method: 'DELETE',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Accept': '*/*',
                    'Authorization': `Bearer ${accessToken}`
                },
                }))
                .catch((error) => {
                console.error(error);
                });
            setTimeout(function(){window.location.reload()}, 1000)
        } else {
            console.log("Delete prevented")
        }
    }

<<<<<<< HEAD
    render() {
        return (
            <div className="GetAttendees">
                <h3>Use this button to get the events!</h3>
                <form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Events!
                    </Button>
                </form>
                {
                  this.state.events &&
                    this.state.events.map((event) => 
                        <Grid key={event.event_id}>
                            <h4>{event.event_name}</h4>
                            <Button onClick={() => {this.deleteEvent(event)}}>Delete</Button>
                            <Link to={{pathname:"/update", state: ['event', event]}}>
                                <Button>Update</Button>
                            </Link>
                        </Grid>
                        
                    )
                }
            </div> 
        )
    }
=======
    
    return (
        <div className="GetAttendees">
            <h3>Use this button to get the events!</h3>
            <form onSubmit={handleSubmit}>
                <Button type="submit" value="Submit" variant="contained">
                    Get Events!
                </Button>
            </form>
            {
                events &&
                events.map((event) => 
                    <Grid key={event.event_id}>
                        <h4>{event.event_name}</h4>
                        <Button onClick={() => {deleteEvent(event)}}>Delete</Button>
                        <Link to={{pathname:"/update/events", state: ['event', event]}}>
                            <Button>Update</Button>
                        </Link>
                    </Grid>
                    
                )
            }
        </div> 
    )
    
>>>>>>> f3f95f88def85be96afb9511bd6e6300f7903154
}

export default GetEvents