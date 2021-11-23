import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'
import { useLocation } from 'react-router';

const request_url = process.env.REACT_APP_API_REQUEST_URL;

export default function AttendeeUpdateForm(props) {
    const location = useLocation()
    const attendee = location.state[1]
    const [firstName, setFirstName] = useState(attendee.firstname)
    const [lastName, setlastName] = useState(attendee.lastname)
    
    const {getAccessTokenSilently} = useAuth0()

    const handleAttendeeSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {firstname: firstName, lastname: lastName}
        const json = JSON.stringify(obj)
        getAccessTokenSilently()
        .then(accessToken => fetch(`${request_url}/attendees/${attendee.attendee_id}`, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Accept': '*/*',
                'Authorization': `Bearer ${accessToken}`
            },
        body: json,
        }))
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error(error);
        });

        setTimeout(function(){window.location.href= "/attendees"}, 1000)
        
    }


        return (
            
                
            <div className="AddGroup">
                        <h3>Please update the fields for the attendee: {attendee.firstname} {attendee.lastname}!</h3>
                        <form onSubmit={handleAttendeeSubmit}>
                            <TextField 
                                id="firstName" 
                                name="firstName"
                                label="First Name" 
                                variant="outlined" 
                                value={firstName} 
                                onChange={e => setFirstName(e.target.value)} 
                                margin="normal"
                            />
                            <br />
                            <TextField 
                                id="lastName" 
                                name="lastName"
                                label="Last Initial" 
                                variant="outlined" 
                                value={lastName} 
                                onChange={e => setlastName(e.target.value)} 
                                margin="normal"
                            />
                            <br />
                            <Button type="submit" value="Submit" variant="contained"> 
                                Submit
                            </Button>
                        </form>
                    </div>
        )
}
