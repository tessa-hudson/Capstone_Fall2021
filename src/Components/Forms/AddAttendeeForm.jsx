import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import '../../Styles/AddAttendeeForm.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function AddAttendeeForm(props) {
    const [firstname, setFirstname] = useState("")
    const [lastname, setLastname] = useState("")
    const {getAccessTokenSilently} = useAuth0()

    const handleSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {firstname: firstname, lastname: lastname}
        const json = JSON.stringify(obj);
        console.log(json);

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
            <div className="AddAttendee">
                <h3>Use this form to add an attendee!</h3>
                <form onSubmit={handleSubmit}>
                    <TextField 
                        id="firstName" 
                        name="firstname"
                        label="First Name" 
                        variant="outlined" 
                        value={firstname} 
                        onChange={(e) => setFirstname(e.target.value)} 
                        margin="normal"
                    />
                    <br />
                    <TextField 
                        id="lastInitial" 
                        name="lastNameInitial"
                        label="Last Initial" 
                        variant="outlined" 
                        value={lastname} 
                        onChange={(e) => setLastname(e.target.value)} 
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

export default AddAttendeeForm