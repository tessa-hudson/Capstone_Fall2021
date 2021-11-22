import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'
import { useLocation } from 'react-router';

const request_url = process.env.REACT_APP_API_REQUEST_URL;

export default function GroupUpdateForm(props) {
   const location = useLocation()
   const group = location.state[1]
   const [groupName, setGroupName] = useState(group.group_name)
   const [groupEventId, setGroupEventId] = useState(group.event_id)
   const [groupTotalPoints, setGroupTotalPoints] = useState(group.total_points)
   
    
    const {getAccessTokenSilently} = useAuth0()

    

    const handleGroupSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {group_name: groupName, event_id: groupEventId, total_points: groupTotalPoints}
        const json = JSON.stringify(obj);

        getAccessTokenSilently()
        .then(accessToken => fetch(`${request_url}/groups/${group.group_id}`, {
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

        setTimeout(function(){window.location.href= "/groups"}, 1000)
    }

        return (
            <div className="AddGroup">
                
               <h3>Please update the fields for the group: {group.group_name}!</h3>
               <form onSubmit={handleGroupSubmit}>
                     <TextField 
                        id="name" 
                        label="Group Name" 
                        variant="outlined" 
                        value={groupName} 
                        onChange={(e) => setGroupName(e.target.value)} 
                        margin="normal"
                     />
                     <br />
                     <TextField 
                        id="name" 
                        label="Event ID" 
                        variant="outlined" 
                        value={groupEventId} 
                        onChange={(e) => setGroupEventId(e.target.value)} 
                        margin="normal"
                     />
                     <br />
                     <TextField 
                        id="name" 
                        label="Group Points" 
                        variant="outlined" 
                        value={groupTotalPoints} 
                        onChange={(e) => setGroupTotalPoints(e.target.value)} 
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

