import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

export default function AttendeeUpdateForm(props) {
    const [firstName, setFirstName] = useState("")
    const [lastName, setlastName] = useState("")
    
    const {getAccessTokenSilently} = useAuth0()

    const handleSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {firstname: firstName, lastname: lastName}
        const json = JSON.stringify(obj)
        getAccessTokenSilently()
        .then(accessToken => fetch(`${request_url}/attendees`, {
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
    }


            
                
    return (
        <div className="AddGroup">
            <div>
                <h3>Use this form to add a new attendee!</h3>
                <form onSubmit={handleSubmit}>
                    <TextField 
                        id="firstname" 
                        label="First Name" 
                        variant="outlined" 
                        value={firstName} 
                        onChange={e => setFirstName(e.target.value)} 
                        margin="normal"
                    />
                    <br />
                    <TextField 
                        id="firstname" 
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
        </div>
    )
    
}
