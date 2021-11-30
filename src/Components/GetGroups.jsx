import React, { useState } from 'react'
import { Button, Grid } from '@mui/material'
import { Link } from "react-router-dom"
import '../Styles/GetGroups.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function GetGroups(props) {

    const [groups, setGroups] = useState([])
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
        setGroups(data.groups);
        console.log('Success:', data.groups);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    const deleteGroup = (group) => {
        if (window.confirm(`Are you sure you want to delete ${group.group_name}`)) {
            getAccessTokenSilently()
            .then((accessToken) => fetch(`${request_url}/groups/${group.group_id}`, {
                method: 'DELETE',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Accept': '*/*',
                    'Authorization': `Bearer ${accessToken}`
                },
                }))
                .catch((error) => {
                console.error(error);
                });
            setTimeout(function(){window.location.reload()}, 1000)
        } else {
            console.log("Delete prevented")
        }
    }


        return (
            <div className="GetGroup">
                <h3>Use this button to get the groups!</h3>
                <form onSubmit={handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Groups!
                    </Button>
                </form>
                {
                  groups &&
                    groups.map((group) => 
                        <Grid key={group.group_id}>
                            <h4>{group.group_name}</h4>
                            <Button onClick={() => {deleteGroup(group)}}>Delete</Button>
                            <Link to={{pathname:"/update/groups", state: ['group', group]}}>
                                <Button>Update</Button>
                            </Link>
                            <Link to={{pathname:"/add-attendees-to-groups", state: ['group', group]}}>
                                <Button>Add Attendees</Button>
                            </Link>
                            <Link to={{pathname:"/remove-attendees", state: ['group', group]}}>
                                <Button>Remove Attendees</Button>
                            </Link>
                            <Link to={{pathname:"/view-attendees", state: ['group', group]}}>
                                <Button>View Attendees</Button>
                            </Link>
                        </Grid>
                    )
                }
            </div> 
        )
}

export default GetGroups
