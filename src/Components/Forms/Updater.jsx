import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import MobileDatePicker from '@mui/lab/MobileDatePicker';
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'

function Updater(props) {
    const [groupName, setGroupName] = useState('')
    const [eventName, setEventName] = useState('')
    const [eventType, setEventType] = useState('')
    const [startDate, setStartDate] = useState(new Date())
    const [endDate, setEndDate] = useState(new Date())
    const [firstName, setFirstName] = useState('')
    const [lastName, setlastName] = useState('')
    const element = useState(props.location.state)
    
    const {getAccessTokenSilently} = useAuth0()
    

    const handleGroupSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {group_name: groupName}
        const json = JSON.stringify(obj);

        fetch(`https://hbda-tracking-backend.azurewebsites.net/groups/${element[0][1].group_id}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        body: json,
        })
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error(error);
        });

        setTimeout(function(){window.location.href= "/groups"}, 1000)
    }

    const handleEventSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        let startDate=startDate.getFullYear() + "-"+ parseInt(startDate.getMonth()+1) +"-"+startDate.getDate();
        let endDate=endDate.getFullYear() + "-"+ parseInt(endDate.getMonth()+1) +"-"+endDate.getDate();
        const obj = {event_name: eventName, event_type: eventType, start_date: startDate, end_date: endDate}
        const json = JSON.stringify(obj);

        fetch(`https://hbda-tracking-backend.azurewebsites.net/events/${element[0][1].event_id}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        body: json,
        })
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error(error);
        });

        setTimeout(function(){window.location.href= "/events"}, 1000)
    }

    const handleAttendeeSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {firstname: firstName, lastname: lastName}
        const json = JSON.stringify(obj)
        getAccessTokenSilently()
        .then(accessToken => fetch(`http://localhost:5000/attendees/${element[0][1].attendee_id}`, {
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

        setTimeout(function(){window.location.href= "/attendees"}, 1000)
        
    }

    
        const { state } = props.location

        return (
            <div className="AddGroup">
                {state[0]==="group" &&
                    <div>
                        <h3>Please update the fields for the group: {state[1].group_name}!</h3>
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
                            <Button type="submit" value="Submit" variant="contained"> 
                                Submit
                            </Button>
                        </form>
                    </div>
                }
                {state[0]==="event" &&
                    <div>
                        <h3>Please update the fields for the event: {state[1].event_name}!</h3>
                        <form onSubmit={handleEventSubmit}>
                            <TextField 
                                id="eventName" 
                                name="eventName"
                                label="Event Name" 
                                variant="outlined" 
                                value={eventName} 
                                onChange={(e) => setEventName(e.target.value)} 
                                margin="normal"
                            />
                            <TextField 
                                id="eventType"
                                name="eventType" 
                                label="Event Type" 
                                variant="outlined" 
                                value={eventType} 
                                onChange={(e) => setEventType(e.target.value)} 
                                margin="normal"
                            />
                            <br />
                            <LocalizationProvider dateAdapter={AdapterDateFns} className="datepicker">
                                <MobileDatePicker
                                    label="Start Date"
                                    inputFormat="MM/dd/yyyy"
                                    value={startDate}
                                    onChange={e => setStartDate(e)}
                                    renderInput={(params) => <TextField {...params} />}
                                />
                            </LocalizationProvider>
                            <LocalizationProvider dateAdapter={AdapterDateFns} >
                                <MobileDatePicker
                                    label="End Date"
                                    inputFormat="MM/dd/yyyy"
                                    value={endDate}
                                    onChange={e => setStartDate(e)}
                                    renderInput={(params) => <TextField {...params} />}
                                    className="datepicker"
                                />
                            </LocalizationProvider>
                            <br />
                            <Button type="submit" value="Submit" variant="contained"> 
                                Submit
                            </Button>
                        </form>
                    </div>
                }
                {state[0]==="attendee" &&
                    <div>
                        <h3>Please update the fields for the attendee: {state[1].firstname} {state[1].lastname}!</h3>
                        <form onSubmit={handleAttendeeSubmit}>
                            <TextField 
                                id="firstName" 
                                name="firstName"
                                label="First Name" 
                                variant="outlined" 
                                value={firstName} 
                                onChange={e => setFirstName(e.target.value)} 
                                margin="normal"
                            />
                            <br />
                            <TextField 
                                id="lastName" 
                                name="lastName"
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
                }
            </div>
        )
}

export default Updater