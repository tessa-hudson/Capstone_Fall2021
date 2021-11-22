import React, { useState } from 'react'
import '../Styles/HomePage.css'
import Scoreboard from './Scoreboard'
import { useAuth0 } from '@auth0/auth0-react'
import { Button } from '@mui/material'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function HomePage(props) {
    const [events, setEvents] = useState(null)
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
    
    return (
        <div className="Home">
            <h1>Welcome to the Camp Clot Not Score Keeper!</h1>
            <h3>Use this button to get the scoreboards!</h3>
            <form onSubmit={handleSubmit}>
                <Button type="submit" value="Submit" variant="contained">
                    Get Scoreboards!
                </Button>
            </form>
            {events && events.map(event => <Scoreboard event={event} key={event.event_id}/>)}
        </div>
        
    )
    
}

export default HomePage