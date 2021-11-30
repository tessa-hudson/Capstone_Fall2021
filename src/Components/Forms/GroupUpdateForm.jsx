import React, { useState, useEffect } from 'react'
import { Button, TextField, MenuItem } from '@mui/material'
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'
import { useLocation } from 'react-router';

const request_url = process.env.REACT_APP_API_REQUEST_URL;

export default function GroupUpdateForm(props) {
   const location = useLocation()
   const group = location.state[1]
   const [groupName, setGroupName] = useState(group.group_name)
   const [groupEventId, setGroupEventId] = useState(group.event_id)
   const [events, setEvents] = useState(null)
   const [status, setStatus] = useState("")
   const [groupTotalPoints, setGroupTotalPoints] = useState(group.total_points)
   
    
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
            <div className="AddGroup" style={{maxWidth:'80%', margin:'0 auto'}}>
                
               <h3>Please update the fields for the group: {group.group_name}!</h3>
               {status === 'Loading' && <div>Loading...</div>}
               {status === 'Error' && <div>There are no events yet</div>}
               {status === 'Success' &&
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
                        id="group-event"
                        value={groupEventId}
                        label="Event"
                        select
                        onChange={e => setGroupEventId(e.target.value)}
                        style={{width: '195px'}}
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
                     <TextField 
                        id="name" 
                        label="Group Points" 
                        variant="outlined" 
                        value={groupTotalPoints} 
                        onChange={(e) => setGroupTotalPoints(e.target.value)} 
                        margin="normal"
                     />
                     <br />
                     <Button type="submit" value="Submit" variant="contained" style={{marginTop:"10px"}}> 
                        Submit
                     </Button>
               </form>
               }
            </div>
        )
}

