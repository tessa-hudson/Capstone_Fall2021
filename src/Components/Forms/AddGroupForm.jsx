import React, { useState, useEffect } from 'react'
import { Button, TextField, MenuItem } from '@mui/material'
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function AddGroupForm(props) {
    const [groupName, setGroupName] = useState("")
    const [eventId, setEventId] = useState("")
    const [events, setEvents] = useState(null)
    const [status, setStatus] = useState("")

    const {getAccessTokenSilently} = useAuth0()

    useEffect(() => {
        setStatus('Loading');
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
        .then(()=>setStatus('Success'))
        .catch((error) => {
        console.error(error);
        setStatus('Error')
        });
    }, [getAccessTokenSilently]);

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
            {status === 'Loading' && <div>Loading...</div>}
            {status === 'Error' && <div>There are no events yet</div>}
            {status === 'Success' &&
            <div>
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
                        id="group-event"
                        value={eventId}
                        label="Event"
                        select
                        onChange={e => setEventId(e.target.value)}
                        style={{width: '195px', marginBottom: '10px'}}
                    >
                        {   events &&
                            events.map((event) => {
                                return (
                                <MenuItem key={event.event_id} value={event.event_id}>{event.event_name}</MenuItem>
                                )
                            })
                        }
                    </TextField>
                    <br />
                    <Button type="submit" value="Submit" variant="contained"> 
                        Submit
                    </Button>
                </form>
            </div>
            }
        </div>
    )
    
}

export default AddGroupForm