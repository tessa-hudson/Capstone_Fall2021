import React, { useState } from 'react'
import { Button } from '@mui/material'
import '../Styles/Scoreboard.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function Scoreboard(props) {
    const [groups, setGroups] = useState(null)
    const {getAccessTokenSilently} = useAuth0()

    const handleSubmit = (event) => {
        
        event.preventDefault() //This prevents the page from refreshing on submit
        
        getAccessTokenSilently()
        .then((accessToken) =>
            fetch(`${request_url}/groups`, {
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
            let filtered = data.groups.filter(group => group.event_id === props.event.event_id)
            setGroups(filtered)
            console.log('Success:', filtered);
        })
        .catch((error) => {
        console.error(error);
        });
    }
   
        return (
            <div className="GetGroup" style={{margin: '20px auto', maxWidth: '80%'}}>
                <h3>{props.event.event_name}</h3>
                <form onSubmit={handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Groups!
                    </Button>
                </form>
                <table>
                    <tbody>
                    {groups && groups.length > 0 && groups.map(group => (
                        <tr key={group.group_id}>
                            <th>{group.group_name}</th>
                            <th>{group.total_points}</th>
                        </tr>
                    ))}
                    </tbody>
                </table>
                {groups && groups.length <= 0 && <h3>No groups for this event</h3>}
            </div> 
        )

}

export default Scoreboard;

  
  