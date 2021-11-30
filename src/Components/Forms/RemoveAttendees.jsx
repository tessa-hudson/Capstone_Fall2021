import React, { useState, useEffect } from 'react'
import { Button } from '@mui/material'
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'
import { useLocation } from 'react-router';
import { default as ReactSelect } from "react-select"
import { components } from "react-select"

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function getOptions(attendees) {
    const optionArray = []
    for (var i=0; i<attendees.length; i++) {
        optionArray.push({value: attendees[i].firstname + ' ' + attendees[i].lastname, label: attendees[i].firstname + ' ' + attendees[i].lastname, id: attendees[i].attendee_id})
    }
    return optionArray
}

function RemoveAttendees(props) {
    const [attendees, setAttendees] = useState([])
    const [status, setStatus] = useState("")
    const [optionSelected, setOptionSelected] = useState(null)
    const location = useLocation()
    const group = location.state[1]

    const {getAccessTokenSilently} = useAuth0()

    useEffect(() => {
        setStatus('Loading');
        getAccessTokenSilently()
        .then((accessToken) =>
            fetch(`${request_url}/attendees`, {
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
        setAttendees(data.attendees);
        console.log('Success:', data.attendees);
        })
        .then(()=>setStatus('Success'))
        .catch((error) => {
        console.error(error);
        setStatus('Error')
        });

        
    }, [getAccessTokenSilently]);

    const handleSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        let attendees = []
        for (var i=0; i<optionSelected.length; i++) {
            attendees.push(optionSelected[i].id)
        }
        const obj = {attendees: attendees, method: 'delete'}
        const json = JSON.stringify(obj)

        console.log(json)

        getAccessTokenSilently()
        .then((accessToken) => fetch(`${request_url}/groups/${group.group_id}/attendees`, {
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

    const Option = (props) => {
        return (
            <div>
                <components.Option {...props}>
                    <input
                        type="checkbox"
                        checked={props.isSelected}
                        onChange={()=>null}
                    />{" "}
                    <label>{props.label}</label>
                </components.Option>
            </div>
        )
    }

    const handleChange = (selected) => {
        setOptionSelected(selected)
    }

    return (
        <div className="AddGroup" style={{maxWidth:'80%', margin:'0 auto'}}>
            {status === 'Loading' && <div>Loading...</div>}
            {status === 'Error' && <div>There are no attendees yet</div>}
            {status === 'Success' &&
            <div>
                <h3>Use this form to remove attendees from {group.group_name}!</h3>
                <form onSubmit={handleSubmit}>
                    <ReactSelect
                        options={getOptions(attendees)}
                        isMulti
                        closeMenuOnSelect={false}
                        hidSelectedOptions={false}
                        component={{
                            Option
                        }}
                        onChange={handleChange}
                        allowSelectAll={false}
                        value={optionSelected}
                    />
                    <Button type="submit" value="Submit" variant="contained" style={{marginTop:"10px"}}> 
                        Submit
                    </Button>
                </form>
            </div>
            }
        </div>
    )
    
}

export default RemoveAttendees