import React, {useState} from 'react'
import { Button, Grid } from '@mui/material'
import { Link } from "react-router-dom"
import '../Styles/GetAttendees.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function GetAttendees(props) {
    const [attendees, setAttendees] = useState([]);
    const {getAccessTokenSilently} = useAuth0()

    const handleSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        
        getAccessTokenSilently()
        .then((accessToken) =>
            fetch(`${request_url}/attendees`, {
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
        setAttendees(data.attendees)
        console.log('Success:', data.attendees);
        })
        .catch((error) => {
        console.error(error);
        });
    
    }

    const deleteAttendee = (attendee) => {
        if (window.confirm(`Are you sure you want to delete ${attendee.firstname} ${attendee.lastname}`)) {

            getAccessTokenSilently()
            .then((accessToken) => fetch(`${request_url}/attendees/${attendee.attendee_id}`, {
                method: 'DELETE',
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
                console.log('Success:', data);
                })
                .catch((error) => {
                console.error(error);
                });
            setTimeout(function(){window.location.reload()}, 1000)
        } else {
            console.log("Delete prevented")
        }
    }

    
    return (
        <div className="GetAttendees">
            <h3>Use this button to get the attendees!</h3>
            <form onSubmit={handleSubmit}>
                <Button type="submit" value="Submit" variant="contained">
                    Get Attendees!
                </Button>
            </form>
            {
                attendees &&
                attendees.map((attendee) => 
                    <Grid key={attendee.attendee_id}>
                        <h4>{attendee.firstname} {attendee.lastname}</h4>
                        <Button onClick={() => {deleteAttendee(attendee)}}>Delete</Button>
                        <Link to={{pathname:"/update/attendees", state: ['attendee', attendee]}}>
                            <Button>Update</Button>
                        </Link>
                    </Grid>
                    
                )
            }
        </div> 
    )
}

export default GetAttendees