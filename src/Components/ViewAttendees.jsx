import React, { useState, useEffect } from 'react'
//import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'
import { useLocation } from 'react-router';

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function ViewAttendees(props) {
    const [mainGroup, setMainGroup] = useState([])
    const [status, setStatus] = useState("")
    const location = useLocation()
    const group = location.state[1]

    const {getAccessTokenSilently} = useAuth0()

    useEffect(() => {
        setStatus('Loading');
        getAccessTokenSilently()
        .then((accessToken) =>
            fetch(`${request_url}/groups/${group.group_id}`, {
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
        setMainGroup(data.attendees);
        console.log('Success:', data.attendees);
        })
        .then(()=>setStatus('Success'))
        .catch((error) => {
        console.error(error);
        setStatus('Error')
        });

        
    }, [getAccessTokenSilently, group.group_id]);

    return (
        <div className="AddGroup" style={{maxWidth:'80%', margin:'0 auto'}}>
            {status === 'Loading' && <div>Loading...</div>}
            {status === 'Error' && <div>There are no attendees yet</div>}
            {status === 'Success' &&
            <div>
                <h3>{group.group_name} attendees!</h3>
                { mainGroup &&
                    mainGroup.map((attendee) => 
                        <p key={attendee.attendee_id}>{attendee.firstname} {attendee.lastname}</p>
                    )
                }
                { !mainGroup[0] &&
                    <p>There are no attendees in this group yet</p>
                }
                
            </div>
            }
        </div>
    )
    
}

export default ViewAttendees