import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function AddGroupForm(props) {
    const [groupName, setGroupName] = useState("")
    const [eventId, setEventId] = useState("")

    const {getAccessTokenSilently} = useAuth0()

    const handleSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {group_name: groupName, event_id: eventId}
        const json = JSON.stringify(obj);

        getAccessTokenSilently()
        .then((accessToken) => fetch(`${request_url}/groups`, {
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
            <h3>Use this form to add a new group!</h3>
            <form onSubmit={handleSubmit}>
                <TextField 
                    id="name" 
                    label="Group Name" 
                    variant="outlined" 
                    value={groupName} 
                    onChange={e => setGroupName(e.target.value)} 
                    margin="normal"
                />
                <br />
                <TextField 
                    id="name" 
                    label="Event ID" 
                    variant="outlined" 
                    value={eventId} 
                    onChange={e => setEventId(e.target.value)} 
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

export default AddGroupForm